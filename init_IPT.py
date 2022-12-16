# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 11:06:36 2018

@author: remy
"""  
import glob #, fnmatch, shutil #, os
    
#####                   paramètres du dépôt 
# fichiers à exécuter localement
execloc_data = [
    {'ext' : '.tex',
     'patterns' : ['*.cours.doc.tex',
                    'A*.doc.tex',
                    'TP*.doc.tex',
                    'S*doc.tex',
                    'M*doc.tex',
                   'exo_*_A.doc.tex'] ,
     'command': ["latexmk", "-f", "-pdf"]},
    {'ext' : '.asy',
     'patterns' : ['*_fig.asy'] ,
     'command': ["asy","-f","pdf"]},
    {'ext' : '.py',
     'patterns' : ['*_fig.py'] ,
     'command': ["python3"]}
    ]
    
    # publish_data : fichiers à publier
publish_data = {'patterns': ['*.cours.doc.pdf',
                             'A*.doc.pdf',
                             'TP*.doc.pdf',
                             'S*doc.pdf',
                             'M*doc.pdf'
                             ],
                'liste' : ['A','TP','S','M','exo','cours'],
                'uri_esp' : 'https://maquisdoc-ipt.nyc3.digitaloceanspaces.com/'}


def idx_data(para):
    """ 
    renvoie les données pour former les requêtes
    cypher pour les fichiers .idx
    au format {'noeuds' : liste de neuds , 'relations' : liste de relations}
    """
    # type de la relation entre un mot clé 'KeyWord' et un document 'Document'
    type_relation = 'QUALIFIE'
    
    #récupérer la liste d'index dabs un fichier d'index (.idx)
    def get_liste_indexes(nom_fic):
        fio = open(nom_fic)
        lili = []
        for lign in fio:
            lign = lign.replace('\indexentry{','')
            lign = lign.split('|hyperpage')[0]
            lign = remplacer(lign)
            lili.append(lign)
        return lili
    
    def remplacer(str):
        """
        renvoie la chaine nettoyée des commandes latex
        """
        lili=[["\\IeC {\\'e}","é"],
              ["\\IeC {\\`e}","è"],
              ["\\IeC {\\`a}","à"],
              ["\\IeC {\\^o}","ô"]
              ]
        str_n = str
        for truc in lili:
            str_n = str_n.replace(truc[0],truc[1])
        return str_n
    
    docs_n = glob.glob('*.idx')
    relations = []
    mots = set()
    data = {'noeuds' : [] , 'relations' : []}
    
    #création de la liste des mots (noeuds)
    #et de la liste des relations mot QUALIFIE document
    for nom_fic in docs_n:
        obj = {}
        prop_car_doc = nom_fic.replace('.idx','.pdf')
        prop_car_doc += '@' + dp_data['nom']
        liste_mots = get_liste_indexes(nom_fic)
        liste_carac_mots = []
        for mot in liste_mots:
            liste_carac_mots.append(mot + '@' + dp_data['nom'])
        #obj['liste_indexes'] = liste_mots
        if len(liste_mots) > 0:
            relations.append([liste_carac_mots,type_relation,[prop_car_doc]])
            mots = mots | set(liste_mots)
    data['relations'] = relations
    mots = list(mots)
    for mot in mots:
        obj = {'label':'KeyWord', 'prop_car' : '', 'props' : []}
        obj['prop_car'] = '"'+ mot + '@' + dp_data['nom'] + '"'
        obj['props'].append(['str',mot])
        data['noeuds'].append( obj )
    #print(data)
    return data
# fin de idx_data


def doc_data(para):
    """
    renvoie les données permettant de former
    les requêtes cypher pour MERGE
    des noeuds de label Document
    """
    data = {'noeuds' : [] , 'relations' : []}
    
    #liste des noms de fichier vérifiant le pattern
    pattern = para['pattern']
    docs_n = glob.glob(pattern)
    for nom_fic in docs_n:
        obj = {'label':'Document', 'prop_car' : '', 'props' : []}
        obj['prop_car'] = '"'+ nom_fic + '@' + dp_data['nom'] + '"'
        props = []
        props.append(['nom', nom_fic])
        props.append(['depot' , dp_data['nom']]) 
        props.append(['uri_img' , publish_data['uri_esp'] + nom_fic])
        obj['props'] = props
        data['noeuds'].append(obj)
    #print('coucou', data)
    return data

# context_data : fichiers (documents) à contextualiser dans la base en graphe
context_data = [
    {'para':{'pattern': '*.cours.doc.pdf', 'type' : 'Cours'},
     'extraire' : doc_data},
    {'para': {'pattern': 'A*.doc.pdf', 'type' : 'Probleme'},
     'extraire' : doc_data},
    {'para' : {'pattern': 'TP*.doc.pdf', 'type' : 'TP'},
     'extraire' : doc_data},
    {'para' : {'pattern': 'exo_*_A.doc.pdf', 'type' : 'Exercice'},
     'extraire' : doc_data},
    {'para' : {'pattern':'*.idx' },
     'extraire' : idx_data}]

    # dp pour dépôt
dp_data = {'nom':'IPT_nicolai',
           'relative_path': '../IPT',
           'execloc_data': execloc_data,
           'publish_data' : publish_data,
           'context_data' : context_data} 


#############          ZONE SECRETE   ####################    
#####       paramètres de connexion à l'espace (de publication web)
sp_connect_data = {'region_name' : 'nyc3',
           'endpoint_url' : 'https://nyc3.digitaloceanspaces.com',
           'aws_access_key_id' : 'QJJW7XIYPHHXDXCW2DS4',
           'aws_secret_access_key' : 'zV256hlsUoZ7XrYwuz1nni28pwtm3oj9a0DMyIzb9u8',
           'bucket' : 'maquisdoc-ipt'}
#####      paramètres de connexion à la base de données en graphe
#local
#bdg_data = {'url' : 'bolt://localhost:7687', 'user': "neo4j", 'pw':"3128"}
# graphenedb
bdg_connect_data = {
    'uri' : "bolt://hobby-emmpngdpepmbgbkeiodbecbl.dbs.graphenedb.com:24786",
    'user': "mimi", 'pw': "b.qzcs8g8XgxeB.Sbc5iAoGjwGi60fr"}
#############   FIN DE ZONE SECRETE    ####################    


    # paramètres de la maintenance
para = {'depot' : dp_data, 'espace' : sp_connect_data, 'bdg' : bdg_connect_data}

