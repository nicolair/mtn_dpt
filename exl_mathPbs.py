# -*- coding: utf-8 -*- 
"""
Module de scripts (à exécuter localement) spécifiques au dépôt d'exercices et complétant les commandes définies dans le manifeste.

Modifié le 15/03/23 @author: remy

Ce module est importé par l'instanciation de l'objet `Execlocal`.  
Les traitements sont exécutés par la fonction `exec()` du module.

J'envisage d'automatiser la création des fichiers `A` à partir des énoncés`E`. Pour le moment, ils sont créés à la main.  
Pour cette hypothétique automatisation, il faudrait:

- Former la liste des énoncés Latex dans le dossier
- Former les fichiers `A` avec énoncé et corrigé (éventuel)
- Former la liste des fichiers à publier
"""
import csv
import glob
import os.path
import re
import scantex


dp_data = {}
dp_data['relative_path'] = '../math-pbs/'
relpath = '../math-pbs/'
lineprefix = "\n \t \t \t"

def exec(data):
    """
    Exécute les traitements spécifiques et complète le journal.

    - Extrait la liste des descriptions
    - Extrait la liste des indexations

    #### Paramètres
    `data`: données d'exécution locale, valeur de `execloc` dans le dictionnaire `manifeste` défini par le module d'initialisation [`init_mathPbs`](init_mathPbs.html).


    #### Renvoie
    
    TYPE : dictionnaire

        `log`: journal de l'exécution des scripts
        `specific_results`: dictionnaire
            `indexations`: liste d'indexations
            `descriptions`: liste de descriptions

    """
    log = lineprefix + 'Scripts du module spécifique (fonction exec())'
    
    # renseigne la propriété .indexations
    idx_path_pattern = data['context_data']['idx_path_pattern']
    indexations = scantex.get_liste_indexations(idx_path_pattern)
    log += lineprefix + str(len(indexations)) + " indexations \n"
    
    # renseigne la propriété .descriptions
    description_pattern = data['context_data']['description']
    descriptions = scantex.get_liste_descriptions(description_pattern)
    log += lineprefix + str(len(descriptions)) + " descriptions \n"
    
    specific_results = {
        'indexations': indexations,
        'descriptions': descriptions}
    
    return {'log': log, 'specific_results': specific_results}
