# -*- coding: utf-8 -*- 
"""
Module de scripts (à exécuter localement) spécifiques au dépôt de problèmes et complétant les commandes définies dans le manifeste.

Modifié le 09/02/23 @author: remy


La fonction `exec()` exécute les tâches spécifiques complémentaires. Elle est appelée lors de l'instanciation de la classe `Execlocal`.

Pour le moment aucun script complémentaire n'est nécessaire. La fonction `exec()` renvoie seulement une ligne dans le journal indiquant la prise en compte de ce module.

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
lineprefix = "\n \t \t"

def exec():
    """
    Complète le journal.

    Returns
    -------
    log : TYPE str
        DESCRIPTION journal de l'exécution des scripts.

    """
    log = lineprefix + 'Scripts du module spécifique (fonction exec())'
    return log
