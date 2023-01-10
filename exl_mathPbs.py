# -*- coding: utf-8 -*- 
"""
Created on Wed Dec  7 07:03:24 2022

@author: remy

Module d'exécution locale de scripts spécifiques au dépôt de problèmes.
    - Forme la liste des énoncés Latex dans le dossier
    - Forme les fichiers A avec énoncé et corrigé (éventuel)
    - Forme la liste des fichiers à publier
"""
import csv
import glob
import os.path
import re
import scantex


dp_data = {}
dp_data['relative_path'] = '../math-pbs/'
relpath = '../math-pbs/'
lineprefix = "\n \t \t"

def exec():
    """
    Vérifie les fichiers "A".

    Returns
    -------
    log : TYPE str
        DESCRIPTION journal de l'exécution des scripts.

    """
    log = lineprefix + 'Scripts du module spécifique (fonction exec())'
    return log
