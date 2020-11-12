# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 08:56:04 2018

Exécution de scripts locaux: 
    création et mise à jour de fichiers Latex
    création de pdf 

@author: remy
"""
import  subprocess, importlib, glob, os.path
import scantex

#commande_list = {".tex":["latexmk", "-f", "-pdf"] ,
#                 ".asy":["asy","-f","pdf"],
#                 ".py":["python3"]}

class Execlocal:
    """
    Exécute les scripts qui doivent l'être.
    Présente les données à publier et à contextualiser
    
    Paramètre depot_data : exemple de mathExos
    ------------------------------------------
      {
        "nom" : "math-exos",
        "relative_path" : "../math-exos/",
        "execloc_module" : "mathExos_feuilles",
        "execloc_data" : [
          {
            "ext" : ".tex",
            "patterns" : ["A_*.tex"] ,
            "command": ["latexmk", "-f", "-pdf"]
          },
          {
            "ext" : ".asy",
            "patterns" : ["E*_*.asy","C*_*.asy"] ,
            "command": ["asy","-f","pdf"]
          },
          {
            "ext" : ".py",
            "patterns" : ["*_fig.py"] ,
            "command": ["python3"]
          }
        ],
        "publish_data" : {
          "patterns": ["A_*.pdf"],
          "liste" : ["A_"]
        },
        "espace" : {
          "region_name" : "fra1",
          "endpoint_url" : "https://fra1.digitaloceanspaces.com",
          "bucket" : "maquisdoc-math",
          "prefix" : "math-exos/"
        },
        "bdg" : {}
      }
    """
    def __init__(self,depot_data):
        self.log = "\n \t Initialisation de la classe Execlocal."
        self.execloc_data = depot_data['execloc_data']
        self.rel_path = depot_data['relative_path']
        self.publish_data = depot_data['publish_data']
        
        #change de répertoire
        maintenance_path = os.getcwd()
        os.chdir(self.rel_path)
        
        
        #importation du module spécifique
        module = depot_data['execloc_module'] 
        try :
            specific = importlib.import_module( module)
            self.log += "\n \t \t Importation du module " + module
            self.log += specific.exec()
        except :
            self.log += "\n \t \t Pas de module à importer"
            
            
        #liste des commandes de compilation à exécuter
        self.cmds_list = self.aexecuter()
        
        #compilations
        self.compil()      
        
        self.apublier = self.apublierImg()  #fichiers à publier dict path : date"""
        
        #retour au répertoire de base
        os.chdir(maintenance_path)        
              
    def aexecuter(self):
        """Renvoie une liste d'objets représentant des commandes de compilation"""
        self.log += "\n \t \t Formation de la liste des commandes de compilation"
        aexec = []
        for type in self.execloc_data:
            obj = {'ext': type['ext'], 
                   'command': type['command'],
                   'fics' : []}
            fics = []
            for paty in type['patterns']:
                paty = self.rel_path + paty
                fics.extend(glob.glob(paty))
            for src in fics:
                if scantex.aexec(src):
                    obj['fics'].append(src)
            #print(obj['fics'])
            aexec.append(obj)
        return aexec
               
    def apublierImg(self):
        """
        Renvoie un dictionnaire
            clé = chemin d'un fichier à publier
            valeur = timestamp du fichier
        """
        self.log += '\t \t Récupération des timesstamp des fichiers à publier \n'
        docs_n = []
        times = {}
        for paty in self.publish_data['patterns']:
            docs_n += glob.glob(paty)
        for nom_doc in docs_n:
                times[self.rel_path + nom_doc] = os.path.getmtime(nom_doc)
        return times
  
        
    def compil(self):
        """
        Exécution des commandes de compilation.
        """
        self.log += '\n \t \t Exécution des compilations \n'
        log = ''
        for obj in  self.cmds_list :
            log += '\t \t \t'
            log += str(len(obj['fics'])) + ' commandes ' + str(obj['command']) + ' fichiers : \n'
            for src in obj['fics']:
                log += '\t \t \t \t' + src
                command = obj['command'] + [src]  
                try :
                    #print(command)
                    subprocess.run(command)
                    log += ' OK \n'
                except subprocess.SubprocessError :
                    log +=' ERREUR dans exécution de la commande \n'
        self.log += log
