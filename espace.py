# -*- coding: utf-8
"""
Module d'interface avec un espace.

Modifié le 12/03/23  @author: nicolair

Un "espace" est un service de stockage analogue au s3 de Amazon mais proposé
par DigitalOcean. Ce module définit la classe `Espace`. Une instanciation de
cette classe réalise la mise à jour de l'espace pour refléter l'état local du
dépôt.
"""
import boto3
import os.path
# import copy
import mimetypes


class Espace:
    """
    Classe Espace.

    """

    def __init__(self, data, apublier_data):
        """
        Initialise la classe et met à jour l'espace.

        Pour les fichiers publiables cad ceux de "apublier_data":

        - récupère les clés associées et leur timestamp dans l'espace
        - si le fichier local est plus récent:
                      upload sur l'espace
        #### Paramètres:
        - data = `manifeste['espace']: dictionnaire codant les données de connexion. Exemple :
        
                {
                    "region_name" : "fra1",
                    "endpoint_url" : "https://fra1.digitaloceanspaces.com",
                    "bucket" : "maquisdoc-math",
                    "prefix" : "math-exos/"
                }
                
            Les données secrètes de connexion sont dans le fichier local
            `~/.aws/credentials`.

        - apublier_data : liste de dictionnaires donnant les timestamps
        des fichiers susceptibles d'être publiés.
            
                [{chemin de fichier local : timestamp du fichier},]

        #### Renvoie

        None.

        """
        connect_data = data['credentials']
        self.log = "\t Initialisation de la classe Espace \n"
        r_n = connect_data['region_name']
        e_u = connect_data['endpoint_url']
        self.bck_nom = connect_data['bucket']
        self.client = boto3.client('s3', region_name=r_n, endpoint_url=e_u)
        s3 = boto3.resource('s3', region_name=r_n, endpoint_url=e_u)
        self.bucket = s3.Bucket(connect_data['bucket'])
        self.prefix = connect_data['prefix']
        self.apublier = apublier_data  # dictio path: date

        self.bck_times = self.get_times()  # dictio key: date

        self.MAJ()

    def get_times(self):
        """
        Renvoie un dictionnaire donnant les dates de modifications des
        fichiers de l'espace.

               clé = key d'un fichier du dépôt dans l'espace
               valeur = date modification
        """
        key_times = {}
        for obj in self.bucket.objects.all():
            if (obj.key.startswith(self.prefix)
                    and len(obj.key) > len(self.prefix)):
                key_times[obj.key] = obj.last_modified
        self.log += '\t \t ' + str(len(key_times)) + " clés dans l'espace \n"
        return key_times

    def del_objs(self, keys):
        """
        Supprime des objets et rend compte dans le journal.
        
        #### Paramètres:
        
        - `keys`: liste des clés à supprimer dans l'espace'

        #### Renvoie
        
        None
        """
        objs = []
        for key in keys:
            objs.append({'Key': key})
        response = self.bucket.delete_objects(Delete={'Objects': objs})
        if 'Deleted' in response:
            self.log += "\n Journal des suppressions de l'espace: \n"
            self.log += 'Deleted : '
            for deleted in response['Deleted']:
                self.log += deleted['Key'] + ', '

    def upload_file(self, path, key):
        """
        Upload un fichier dans l'espace.

        Avec un ACL public et un Content-Type déduit de l'extension.

        #### Parametres
        
        - path : chemin du fichier à uploader dans l'espace.
        - key : clé du fichier uploadé dans l'espace.

        Renvoie
        -------
        None.

        """
        file_name = os.path.basename(path)
        file_mime_type, encoding = mimetypes.guess_type(file_name)
        self.bucket.upload_file(path, key,
                                ExtraArgs={'ACL': 'public-read',
                                           'ContentType': file_mime_type})

    def MAJ(self):
        """
        Mise à jour de l'espace.

        Avec self.bck_times et self.apublier:
              - supprime dans l'espace les clés
                  qui ne correspondent pas à un fichier
              - si fichier plus récent que clé
                  upload du fichier dans la clé
        """
        key_times = self.bck_times
        fic_times = self.apublier

        # supprimer les keys qui ne sont pas des fics
        fics = [os.path.basename(t) for t in fic_times]
        a_supprimer = []
        for key in key_times:
            if os.path.basename(key) not in fics:
                a_supprimer.append(key)
        self.log += "\t \t " + str(len(a_supprimer)) + " clés à supprimer \n"
        self.del_objs(a_supprimer)

        # mettre à jour les keys correspondant à des fics
        self.log += "\t \t  clés à créer ou mettre à jour \n"
        for path in fic_times:
            file_name = os.path.basename(path)
            key_a_updater = self.prefix + file_name
            fic_a_updater_time = fic_times[path]
            #self.log += '\t \t '  ajoute des espaces inutiles si rien à updater
            if key_a_updater in key_times:
                key_a_updater_time = key_times[key_a_updater].timestamp()
                if fic_a_updater_time > key_a_updater_time:
                    self.log += key_a_updater + " : upload (maj)\n "
                    self.upload_file(path, key_a_updater)
            else:
                self.log += key_a_updater + " : upload (créer) \n "
                self.upload_file(path, key_a_updater)
        self.log += '\n'

    """
    Méthodes qui ne sont pas utilisées

    def put_objs(self, keys):
        #Place (put) les objets de la liste keys dans l'espace.
        #Cette méthode n'est pas utilisé actuellement, remplacée par upload'

        jrnl = ''
        bck = self.bck_nom
        acl = 'public-read'
        ct = 'application/pdf'
        for key in keys:
            bdy = open(key, mode='rb')
            response = self.client.put_object(ACL=acl, Body=bdy, Bucket=bck,
                                              Key=key, ContentType=ct)
            print(str(response))
            jrnl += '\n ' + key + ' : ' + str(response) + '\n'
        return jrnl

    def get_private_objs(self):
        #renvoie la liste des objets avec un acl privé

        bck = self.bck_nom
        response = self.client.list_objects_v2(Bucket=bck, MaxKeys=1000)
        objs = [content['Key']for content in response['Contents']]
        objs_p = copy.copy(objs)
        for key in objs:
            response = self.client.get_object_acl(Bucket=bck, Key=key)
            for grant in response['Grants']:
                permission = grant['Permission']
                grantee = grant['Grantee']
                # print(key, grantee)
                if 'URI' in grantee:
                    grp = os.path.basename(grantee['URI'])
                    # print(key, grp, permission)
                    if (grp == 'AllUsers') and (permission == 'READ'):
                        objs_p.remove(key)
        return objs_p

    def list_buckets(self):
        response = self.client.list_buckets()
        spaces = [space['Name'] for space in response['Buckets']]
        print("Spaces List: %s" % spaces)

    def get_objs(self):
        bck = self.bck_nom
        response = self.client.list_objects_v2(Bucket=bck, MaxKeys=1000)
        objs_t = [[content['Key'], content['LastModified'].timestamp()]
                  for content in response['Contents']]
        return objs_t

    """
