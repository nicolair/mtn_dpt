#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La contextualisation du dépôt d'exercices  s'assure que la base en graphe reflète les exercices et leurs méta-données locales. Ces méta-données sont définies par l'auteur c'est à dire écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Modifié le 05/03/23 @author: remy

La fonction `exec()` est appelée lors de l'instanciation de la classe `Maquis`. Elle maintient cette cohérence en exécutant des requêtes cypher.


#### Noeud associé à un problème.

"""
import neo4j

def exec(self):
    print("coucou de exec() dans bdg_mathExos.py")
    
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)
    
    log = ""
    return log
