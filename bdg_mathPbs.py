#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contextualisation du dépôt de problèmes.

Modifié le 13/02/23 @author: remy

Elle consiste à s'assurer que la base en graphe reflète les problèmes et leurs méta-données. Ces méta-données sont définies par l'auteur c'est à dire écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Quelles sont les méta-données définies par l'auteur d'un problème?
- une description
- des index

Un utilisateur autre que l'auteur doit pouvoir aussi associer des méta-données à un problème. La base en graphe reflète une méta-donnée de manière différente selon qu'elle est définie par l'auteur ou par un utilisateur. 

La définition de méta-données par un utilisateur n'est pas encore implémentée.

#### Noeud et description associés à un problème.

L'auteur définit une description d'un problème en l'insérant entre des tags dans le fichier Latex de l'énoncé. Exemple avec le début de `Eprob4.tex`

    %<dscrpt>Lancers de pièces.</dscrpt>
    On dispose de deux pièces de monnaie discernables, désignées dans la suite
    de l'exercice par \og pièce 1\fg~ et \og pièce 2\fg. On ...

Un noeud labélisé `Document` est associé au problème `prob4`. La description définie dans le code source est la propriété `description` du noeud.

Les lignes suivantes présentent la requête cypher pour extraire ce noeud 

    MATCH (d:Document {typeDoc:"problème", titre:"prob4"}) RETURN d
    
et le noeud renvoyé

    {
    "identity": 7214,
    "labels": [
        "Document"
    ],
    "properties": {
        "date": "2018-05-06T21:36:11Z",
        "titre": "prob4",
        "urlSrcEnon": "https://github.com/nicolair/math-pbs/blob/master/Eprob4.tex",
        "typeDoc": "problème",
        "urlSrcCorr": "https://github.com/nicolair/math-pbs/blob/master/Cprob4.tex",
        "description": "Lancers de pièces.",
        "url": "https://maquisdoc-math.fra1.digitaloceanspaces.com/maths-pbs/Aprob4.pdf"
    },
    "elementId": "7214"
    }
    
Une description insérée par un autre utisateur serait contenue dans la propriété `texte` d'un noeud labélisé `Commentaire` et relié au document `prob4` par une arête labélisée `DÉCRIT`. Ceci n'est pas encore implémenté.

#### Index associés à un problème.

Les index sont définis dans la source LateX par la commande `\index`. Lors de la compilation, un fichier `.idx` est créé qui permet localement d'associer l'index et le problème. Du côté de la base en graphe, un index est un noeud labelisé `Concept`. Une arête labélisée `INDEXE` issue du noeud associé au problème pointe vers le noeud associé à l'index.

Si on considère l'arête dans l'autre sens c'est à dire pointant de l'index vers le problème, un index apparait commun un mot-clé.  
Un mot-clé défini par un utilisateur sera défini avec une arète dont la source est le noeud représentant le mot et dont la cible est le noeud représentant le problème. Cette fonctionnalité n'est pas encore implémentée et les labels du noeud représentant le mot et de l'arête ne sont pas fixés. 

La fonction `exec()` exécute les tâches spécifiques complémentaires. Elle est appelée lors de l'instanciation de la classe `Maquis`.

Tâches de `exec()`

- Récupération des données spécifiques
  - descriptions
  - index

"""
