# -*- coding: utf-8 -*- 
"""
Module de scripts (à exécuter localement) spécifiques au dépôt de cours et complétant les commandes définies dans le manifeste.

Modifié le 30/03/23 @author: remy

Ce module est importé par l'instanciation de l'objet `Execlocal`.  
Les traitements sont exécutés par la fonction `exec()` du module.

"""
import csv
import glob
import os.path
import re
import scantex


dp_data = {}
dp_data['relative_path'] = '../math-cours/'
relpath = '../math-pbs/'
lineprefix = "\n \t \t \t"

def exec(data):
    """
    Exécute les traitements spécifiques et complète le journal.

    - Extrait la liste des indexations
    - Associe le nom du fichier à son titre

    #### Paramètres
    `data`: données d'exécution locale, valeur de `execloc` dans le dictionnaire `manifeste` défini par le module d'initialisation [`init_mathPbs`](init_mathPbs.html).


    #### Renvoie
    
    TYPE : dictionnaire

        `log`: journal de l'exécution des scripts
        `specific_results`: dictionnaire
            `indexations`: liste d'indexations
            `titres`: associe nom fichier au titre. structure à préciser

    """
    log = lineprefix + 'Scripts du module spécifique (fonction exec())'
    
    # renseigne la propriété .indexations
    idx_path_pattern = data['context_data']['idx_path_pattern']
    indexations = scantex.get_liste_indexations(idx_path_pattern)
    log += lineprefix + str(len(indexations)) + " indexations \n"
    
    # renseigne la propriété .titres
    cours_path_pattern = data['context_data']['cours_path_pattern']
    noms = []
    noms.extend(glob.glob(cours_path_pattern))
    titres = []
    for nom in noms:
        if "_expo" not in nom:
            titre = scantex.get_entre_tags(nom,'\debutcours{','}')
            titres.append([nom, titre])
    titres.sort(key=lambda paire: paire[0])
    
    specific_results = {
        'indexations': indexations,
        'titres': titres
    }
    
    return {'log': log, 'specific_results': specific_results}
