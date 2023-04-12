# -*- coding: utf-8 -*-
"""
Ce module code et présente le *manifeste* du dépôt `math-cours`.

Modifié le 30/03/23 @author: remy

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

Les fichiers "C" sont des textes de cours. Le nom d'un fichier de ce type est de la forme `Cnnnn.tex` où "nnnn" désigne 4 (ou 5)chiffres. La raison de cette convention se perd dans l'histoire du maquis et ne correspond à rien actuellement. Le titre pertinent du texte est à extraire directement du fichier LateX.  
Comme pour les autres dépôts, les fichiers `Cnnnn_1.asy`, `Cnnnn_1.pdf`, ... sont attachés à des figures du texte.

Les fichiers "S" sont formés à partir du programme 2018 de la classe de MPSI et permettent de constituer les 30 programmes de colles de la classe de MPSI B en 2019-2020. Ces fichiers n'ont pas à être modifiés.

### Traitement local

- Avant publication
    - les fichiers "C" sont compilés en pdf et placés dans `pdfdir` 
    
- Avant contextualisation
    - Les fichiers "C" sont scannés pour associer les titres aux noms des fichiers.
    - Les fichiers `*.idx` sont scannés pour extraire les index.


### Publication

Voir le sous-module [`espace`](espace.html) pour la mise en oeuvre de la publication. 

Ce sous-module ne définit en clair que les paramètres publics du serveur de publication.
Les credentials secrets sont définis dans le fichier local `~/.aws`.


### Contextualisation
#### Noeuds
Un noeud labélisé `Document` est associé à un texte de cours "C" et caractérisé par sa propriété titre qui est égale au titre dans le fichier Latex et pas au nom du fichier.  

Des noeuds sont aussi associés aux fichiers "S" mais ils ne seront pas mis à jour à cours terme et ne seront pas modifiés.
#### Arêtes

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
        'patterns': ['pdfdir/C*.pdf', 'htmldir/*']
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
