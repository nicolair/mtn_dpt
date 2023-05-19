# -*- coding: utf-8 -*-
"""
Ce module code et présente le *manifeste* du dépôt `math-cours`.

Modifié le 15/05/23 @author: remy

Le manifeste d'un dépôt décrit
- les conventions de nommage des fichiers permettant leur traitement local avant publication et contextualisation,
- les commandes de traitement local,
- les données du serveur de publication spécifique au dépôt,
- les données du serveur de contextualisation spécifique au dépôt.


Ce module définit un dictionnaire `manifeste`.
- `manifeste['nom']` présente le nom du dépôt : 'math-pbs'
- `manifeste['execloc']` présente les paramètre de traitement local
- `manifeste['espace']` présente les paramètres de publication
- `manifeste['context']` présente les paramètres de contextualisation

### Conventions de nommage
Ce dépôt comprend deux types de fichiers LateX dont les noms commencent par `C` (désignés comme fichiers "C") ou par `S` (fichiers "S").

Les fichiers "C" sont des textes de cours. Le nom d'un fichier de ce type est de la forme `Cnnnn.tex` où "nnnn" désigne 4 (ou 5) chiffres. La raison de cette convention se perd dans l'histoire du maquis et ne correspond à rien actuellement. Le titre pertinent du texte est à extraire directement du fichier LateX.
Comme pour les autres dépôts, les fichiers `Cnnnn_1.asy`, `Cnnnn_1.pdf`, ... sont attachés à des figures du texte.

Les fichiers "S" sont formés à partir du programme 2018 de la classe de MPSI et permettent de constituer les 30 programmes de colles de la classe de MPSI B en 2019-2020. Ces fichiers n'ont pas à être modifiés.

### Traitement local
Voir les sous-modules [execlocal](execlocal.pdf) et [exl_mathCours](exl_mathCours.html) pour la mise en oeuvre de l'exécution locale.

- Avant publication
    - les fichiers "C" sont compilés en pdf et placés dans `pdfdir` 
    
- Avant contextualisation
    - Les fichiers "C" sont scannés pour associer les titres aux noms des fichiers.
    - Les fichiers `*.idx` sont scannés pour extraire les index.

### Publication

Voir le sous-module [`espace`](espace.html) pour la mise en oeuvre de la publication. 

Les fichiers `C` compilés de `pdfdir` sont maintenus dans l'espace.
'
Ce sous-module ne définit en clair que les paramètres publics du serveur de publication.
Les credentials secrets sont définis dans le fichier local `~/.aws`.


### Contextualisation
Voir les sous-modules [graphdb](graphdb.html) et [bdg_mathCours](bdg_mathCours.html) pour la mise en oeuvre de la contextualisation.

#### Noeuds
Un noeud labélisé `Document` avec la propriété `typeDoc` égale à "cours" est associé à un texte de cours "C". Il est caractérisé par sa propriété titre qui est égale au titre dans le fichier Latex. Le nom du fichier source apparait dans les propriétés `url` ou `urlSrc` et permet aussi de caractériser le noeud.

Des noeuds sont aussi associés aux fichiers "S" mais ils ne seront pas mis à jour à court terme et ne seront pas modifiés.

Un noeud labélisé `Concept` est associé à un index présent dans le fichier Latex. Si le concept n'est pas déjà défini dans le graphe, la propriété `typeConcept` est égale à "index Latex".

#### Arêtes
Une indexation Latex est associée à une arête labelisée `INDEXE` entre le noeud Cours et le noeud Concept. Exple Cypher pour renvoyer ces relations:

    MATCH r = (d:Document {typeDoc:"cours"})-[:INDEXE]-> (c:Concept {typeConcept:"index Latex"})
    RETURN r

### Scénarios de travail admissibles
- modifier un fichier `C`
- ajouter un index dans un fichier `C` 
"""

import os

# nouvelle organisation

execloc = {
    'relative_path': '../math-cours/',
    'modulespec': 'exl_mathCours',
    'commandes': [
        {'ext': '.tex',
         'patterns': ['C*.tex'],
         'imgdir': 'pdfdir/',
         'imgext': '.pdf',
         'command': [
             "latexmk",
             "-pdf",
             "-emulate-aux-dir",
             "-auxdir=auxdir",
             "-outdir=pdfdir"
             ]
         },
         {'ext': '.asy',
          'patterns': ['*_fig.asy'],
          'imgdir': '',
          'imgext': '.pdf',
          'command': [
              "asy",
              "-f",
              "pdf"
              ]
          },
          {'ext': '.py',
           'patterns': ['*_fig.py'],
           'imgdir': '',
           'imgext': '.pdf',
           'command': [
               "python3"
               ]
           },
        ],
    'publish_data': {
        'patterns': ['pdfdir/C*.pdf', 'S*.pdf']
        },
    'context_data': {
        'idx_path_pattern': 'C*.idx',
        'cours_path_pattern': 'C*.tex'
        }
    }

espace = {
    'credentials': {
        'region_name': 'fra1',
        'endpoint_url': 'https://fra1.digitaloceanspaces.com',
        'bucket': 'maquisdoc-math',
        'prefix': 'math-cours/',
                   },
        'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'
    }

context = {
    'credentials': {
        'URI': os.getenv('NEO4J_URL'),
        'user': os.getenv('NEO4J_USERNAME'),
        'password': os.getenv('NEO4J_PASSWORD')
        },
    'modulespec': 'bdg_mathCours'
    }

manifeste = {'nom': 'math-cours',
             'execloc': execloc,
             'espace': espace,
             'context': context}
