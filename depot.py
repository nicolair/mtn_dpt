# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:11:02 2017

@author: nicolair

"""
import execlocal, espace

class Depot():
    """
    Classe représentant un dépot.
    
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
        """
        Instancie une classe d'exécution locale
        Instancie une classe de publication
        Instancie une classe de contextualisation
        """
        self.log = "\n \t Initialisation de la classe Depot : "
        
        self.nom = depot_data['nom']
        self.rel_path = depot_data['relative_path'] 
        self.execloc_data = depot_data['execloc_data']
        self.publish_data = depot_data['publish_data']
        #self.context_data = depot_data['context_data']
        
        #classe d'exécution locale
        exl = execlocal.Execlocal(depot_data)
        self.apublier = exl.apublier
        self.log += exl.log 
        
        #classe de publication
        esp = espace.Espace(depot_data['espace'],self.apublier)
        self.log += esp.log 
        #classe de contextualisation
        
        
        # chgt de dossier pour se placer dans celui du dépôt
        
        
          
    def acontextualiser(self):
        """
        Renvoyer les données à mettre à jour dans le graphe neo4j
        """
        noeuds = [] 
        relations = []
        for obj in self.context_data:
            truc = obj['extraire'](obj['para'])
            noeuds.extend(truc['noeuds'])
            relations.extend(truc['relations'])
        return {'noeuds' : noeuds , 'relations' : relations }

