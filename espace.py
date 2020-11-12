# -*- coding: utf-8
"""
Created on Wed Jul  5 07:48:13 2017

@author: nicolair

Module d'interface avec un espace.

Un "espace" est un service de stockage analogue au s3 de Amazon mais proposé 
par DigitalOcean.
"""
import boto3, os.path, copy

class Espace :
    """Paramètres:
        ----------
        connect_data: dictionnaire. Exemple : 
          {
            "region_name" : "fra1",
            "endpoint_url" : "https://fra1.digitaloceanspaces.com",
            "bucket" : "maquisdoc-math",
            "prefix" : "math-exos/"
          }

        apublier_data: liste de dictionnaires
            [{chemin de fichier local : timestamp du fichier},]
    """
    def __init__(self,connect_data,apublier_data):
        """Pour les fichiers de apublier_data:
                - récupère les clés correspondantes et leur timestamp dans l'espace
                - si le fichier local est plus récent:
                      upload sur l'espace
        """
        self.log = "\t Initialisation de la classe Espace \n"
        r_n = connect_data['region_name']
        e_u = connect_data['endpoint_url']
        self.bck_nom = connect_data['bucket']
        self.client = boto3.client('s3', region_name=r_n, endpoint_url=e_u)
        s3 = boto3.resource('s3',region_name=r_n, endpoint_url=e_u)
        self.bucket = s3.Bucket(connect_data['bucket'])
        self.prefix = connect_data['prefix']
        self.apublier = apublier_data #dictio path: date
        
        self.bck_times = self.get_times() #dictio key: date
        
        self.MAJ()
        
    def get_times(self):
        """Renvoie un dictionnaire:
               clé = key d'un fichier du dépôt dans l'espace
               valeur = date modification"""
        key_times = {}
        for obj in self.bucket.objects.all():
            if obj.key.startswith(self.prefix) and len(obj.key) > len(self.prefix):
                key_times[obj.key] = obj.last_modified
        self.log += '\t \t ' + str(len(key_times)) + " clés dans l'espace \n"
        return key_times
        
        
    def list_buckets(self):
        response = self.client.list_buckets()
        spaces = [space['Name'] for space in response['Buckets']]
        print("Spaces List: %s" % spaces)
        
    def get_objs(self):
        bck = self.bck_nom
        response = self.client.list_objects_v2(Bucket=bck, MaxKeys=1000)
        objs_t = [[content['Key'],content['LastModified'].timestamp()] for content in response['Contents']]
        return objs_t

    def get_private_objs(self):
        """
        renvoie la liste des objets avec un acl privé
        """
        bck = self.bck_nom
        response = self.client.list_objects_v2(Bucket=bck, MaxKeys=1000)
        objs = [content['Key']for content in response['Contents']]
        objs_p = copy.copy(objs)
        for key in objs:
            response = self.client.get_object_acl(Bucket=bck, Key=key)
            for grant in response['Grants']:
                permission = grant['Permission']
                grantee = grant['Grantee']
                #print(key, grantee)
                if 'URI' in grantee :
                    grp = os.path.basename(grantee['URI'])
                    #print(key, grp, permission)
                    if (grp == 'AllUsers') and (permission == 'READ'):
                        objs_p.remove(key)
        return objs_p

    def del_objs(self,keys):
        """
        supprime les objets dont les clés sont les valeurs de la liste keys et renvoie un message
        """
        objs=[]
        for key in keys:
            objs.append({'Key':key})
        response = self.bucket.delete_objects(Delete={'Objects':objs})
        if 'Deleted' in response:
            self.log += "\n Journal des suppressions de l'espace: \n" 
            self.log += 'Deleted : '
            for deleted in response['Deleted']:
                self.log += deleted['Key'] + ', '
            
    def upload_file(self,file,key):
        self.bucket.upload_file(file, key, {'ACL': 'public-read'})
        #self.log += "upload : " + file + ' ' + key +'\n'
        
    
    def put_objs(self,keys):
        """
        place (put) les objets de la liste keys dans l'espace
        """
        jrnl = ''
        bck = self.bck_nom
        acl = 'public-read'
        ct = 'application/pdf'
        for key in keys:
            bdy = open(key,mode='rb')
            response = self.client.put_object(ACL=acl,Body=bdy,Bucket=bck,
                                              Key=key,ContentType=ct)
            print(str(response))
            jrnl += '\n ' + key + ' : '+ str(response) + '\n'
        return jrnl

    def MAJ(self):
        """Avec self.bck_times et self.apublier:
              - supprime dans l'espace les clés qui ne correspondent pas à un fichier
              - si fichier plus récent que clé
                  upload du fichier dans la clé
        """
        key_times = self.bck_times
        fic_times = self.apublier
        
        #supprimer les keys qui ne sont pas des fics
        fics = [os.path.basename(t) for t in fic_times]
        a_supprimer = []
        for key in key_times:
            if os.path.basename(key) not in fics:
                a_supprimer.append(key)
        self.log += "\t \t " + str(len(a_supprimer)) + " clés à supprimer \n"
        self.del_objs(a_supprimer)
        
        #mettre à jour les keys correspondant à des fics
        for path in fic_times:
            key_a_updater = self.prefix + os.path.basename(path)
            fic_a_updater_time = fic_times[path]
            log = '\t \t '
            try :
                key_a_updater_time = key_times[key_a_updater].timestamp()
                if fic_a_updater_time > key_a_updater_time:
                    log += key_a_updater + " : upload (maj): " 
                    self.upload_file(path, key_a_updater)
                else:
                    log += key_a_updater + ' : à jour'
            except:
                key_a_updater = self.prefix + os.path.basename(path)
                log += key_a_updater + " : upload (créer): "
                self.upload_file(path, key_a_updater)
            log += '\n'
            self.log += log
 
        
        
    def MAJ_old(self):
        docs = self.apublier
        docs_n = docs[0] # noms
        doc_time = docs[1] # times
        
        #former la liste des objets
        objs = self.get_objs()
        #liste d'objets à supprimer
        objs_del = []
        #liste d'objets à placer
        objs_put = []
        
        for obj in objs:
            nom_obj = obj[0]
            time_obj = obj[1]
            if nom_obj not in docs_n:
                #supprimer l'objet de l'espace
                objs_del.append(nom_obj)
            else:
                if time_obj < doc_time[nom_obj]:
                    # mettre à jour l'objet de l'espace
                    objs_put.append(nom_obj)
                #supprimer le document de la liste
                docs_n.remove(nom_obj)
        #placer ceux qui restent(ils ne sont pas dans le space)
        for nom_obj in docs_n:
            objs_put.append(nom_obj)
        
        #suppression des objets
        #attention limité à 1000 objets
        jrnl_supprimer = '\n Journal de "SUPPRIMER" \n'
        if len(objs_del) > 0 :
            jrnl_supprimer += self.del_objs(objs_del)
        else:
            jrnl_supprimer += 'pas d\'objets à supprimer'
            
        #mise à jour des objets
        jrnl_placer = '\n Journal de "PLACER" \n'
        if len(objs_put) > 0 :
            jrnl_placer += self.put_objs(objs_put)
        else:
            jrnl_placer += 'pas d\'objets à placer'
        
        # vérification des autorisations des objets (facultatif)
        #objs_private = sp.get_private_objs()
        #jrnl_autoriser = '\nJournal de "AUTORISER" \n'
        #jrnl_autoriser += 'liste des objets à rendre publics \n'
        #jrnl_autoriser += str(objs_private)
        # écrire une méthode pour rendre publics les objets d'une liste
        
        jrnl = {}
        jrnl['supprimer'] = jrnl_supprimer
        jrnl['placer'] = jrnl_placer
        #jrnl['autoriser'] = jrnl_autoriser
        return jrnl
        
