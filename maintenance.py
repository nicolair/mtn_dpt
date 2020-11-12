#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 05:46:12 2020

@author: remy

Maintenance des dépôts.

Initialisation
--------------
    avec des fichiers .json
      maintenance.json : liste des noms (nomdpt) des dépôts
      nomdpt.json : données spécifiques au dépôt nomdpt
    
Modules utilisés
----------------
    depot : contenant la classe Depot
    execlocal : classe Execlocal d'exécution de scripts locaux
    modules spécifiques aux dépôts, nom lu dans l'initialisation
    scantex : outils d'analyse de fichiers LateX
    espace : classe Espace représentant un espace de publication
"""
import json
import depot

def MAJ():
  """Exécute la mise à jour de chaque dépôt"""
  journal = ''
  #liste des dépôts
  fifi_list_dpt = open('maintenance.json')
  
  #pour chaque dépôt
  for nom_dpt in json.load(fifi_list_dpt):
    journal += '\n Mise à jour de ' + nom_dpt + '\n'
    
    #instanciation d'un objet Depot
    #données spécifiques
    fifi_dpt_data = open(nom_dpt + '.json')
    para = json.load(fifi_dpt_data)
    
    dp = depot.Depot(para)
    journal += dp.log
    
  return journal
    

if __name__ == '__main__' :
    journal = MAJ()
