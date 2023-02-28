"""
Ce module code le manifeste du dépôt `math-pbs`. 

Modifié le 17/02/23 @author: remy

Le manifeste d'un dépôt décrit
- les conventions de nommage des fichiers permettant leur traitement local avant publication et contextualisation,
- les commandes de traitement local,
- les données du serveur de publication spécifique au dépôt,
- les données du serveur de contextualisation spécifique au dépôt.


Ce module définit un dictionnaire `data`.
- `data['nom']` présente le nom du dépôt : 'math-pbs'
- `data['execloc']` présente les paramètre de traitement local
- `data['espace']` présente les paramètres de publication
- `data['context']` présente les paramètres de contextualisation

### Conventions de nommage

L'élément essentiel de ce dépôt est un problème. Un problème particulier est caractérisé par une chaîne de caractère (appelé ici son titre) qui évoque vaguement son thème.

Le nom des fichiers LateX associés à un problème est formé à partir de son titre:
- précédé par `E` pour un énoncé et `C` pour un corrigé (sources LateX),
- précédé par `A` pour le fichier à compiler en pdf du problème corrigé.

Exemple `alglin15` est le titre d'un problème d'algèbre linéaire.
L'énoncé est `Ealglin15.tex`, le corrigé est `Calglin15.tex`.
Le fichier à compiler présentant le problème corrigé est `Aalglin15.tex`.

Énoncés ou corrigés peuvent utiliser des fichiers annexes (figures, codes,..)
dont le nom est obtenu en ajoutant `_numéro` à la fin avant l'extension.

Exemple `p3impko` est le titre d'un problème portant sur le thème
"période 3 implique chaos". Le corrigé comporte une figure `Cp3impko_1.pdf`
formée à partir de la source `Cp3impko_1.asy` écrit en `asymptote` (langage
de création de figure) compilé en pdf. L'énoncé comporte aussi une figure
`Ep3impko_1.pdf` formée à partir de `Ep3impko_1.asy`

Pour le moment, un fichier dont le nom est `Atitre.tex` est édité à la main.
Remarque, dans le dépôt d'exercices, les fichiers analogues sont formés et mis à jour par la maintenance.

###  Traitement local 

- Avant publication
  - Les fichiers `Atitre.tex` sont compilés en pdf et placés dans `pdfdir`.

- Avant contextualisation
 - Les énoncés sources sont scannés pour extraire les descriptions (voir contextualisation).

 - Les fichiers `*.idx` sont scannés pour extraire les index (voir contextualisation).

Voir les sous modules [`execlocal`](execlocal.html), [`exl_mathPbs`](exl_mathPbs.html) pour la mise en oeuvre des traitements locaux et les résultats passés aux classes de publication et de contextualisation.

### Publication 

Les fichiers images `Atitre.pdf` dans `pdfdir` sont téléchargés dans l'espace associé au dépôt.

Voir le sous-module [`espace`](espace.html) pour la mis en oeuvre de la publication. 

Ce sous-module ne définit en clair que les paramètres publics du serveur de publication.
Les credentials secrets sont définis dans le fichier local `~/.aws`.

### Contextualisation 

#### Noeuds

À chaque problème correspond un unique noeud dans la base en graphe caractérisé par son label et ses propriétés `typeDoc` et `titre`. L'exemple suivant de requête cypher renvoie l'unique noeud associé au problème de titre "prob4".

    MATCH (d:Document {typeDoc:"problème", titre:"prob4"}) RETURN d
    
#### Descriptions

Chaque problème comporte une *description* codée en dur dans la première ligne de la source de son énoncé entre les tags `%<dscrpt>` et `%</dscrpt>`. Le début de `Eprob4.tex` est

    %<dscrpt>Lancers de pièces.</dscrpt>
    On dispose de deux pièces de monnaie discernables, désignées dans la suite
    de l'exercice par \og pièce 1\fg~ et \og pièce 2\fg. On ...

Le noeud renvoyé par la requête précédente est

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

La description du problème est la propriété `description` de ce noeud.

#### Index

Les index sont définis dans la source LateX par la commande `\index`. Lors de la compilation, un fichier `.idx` est créé qui permet localement d'associer l'index et le problème. Du côté de la base en graphe, un index est un noeud labelisé `Concept`. Une arête labélisée `INDEXE` issue du noeud associé au problème pointe vers le noeud associé à l'index.

Si on considère l'arête dans l'autre sens c'est à dire pointant de l'index vers le problème, un index apparait comme un mot-clé.  
Un mot-clé défini par un utilisateur sera défini avec une arète dont la source est le noeud représentant le mot et dont la cible est le noeud représentant le problème. Cette fonctionnalité n'est pas encore implémentée et les labels du noeud représentant le mot et de l'arête ne sont pas fixés. 

Voir les sous modules [`graphdb`](graphdb.html), [`bdg_mathPbs`](bdg_mathPbs.html) pour la mise en oeuvre de la contextualisation.

Ce sous-module ne définit en clair que les paramètres publics du serveur de contextualisation.
Les credentials secrets sont définis dans les variables d'environnement `NEO4J_URL` et `NEO4J_PASSWORD`.

"""

import os
"""
ancienne version obsolète
# fichiers à compiler localement
execloc_data = [
    {'ext': '.tex', 'patterns': ['A*.tex'],
     'imgdir': 'pdfdir/', 'imgext': '.pdf',
     'command': ["latexmk", "-pdf", "-emulate-aux-dir",
                 "-auxdir=auxdir", "-outdir=pdfdir"]},
    {'ext': '.asy', 'patterns': ['*_fig.asy'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["asy", "-f", "pdf"]},
    {'ext': '.py', 'patterns': ['*_fig.py'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["python3"]},
    ]

# modules spécifiques
execloc_module = 'exl_mathPbs'
bdg_module = 'bdg_mathPbs'

# publish_data : fichiers à publier
publish_data = {
    'patterns': ['pdfdir/A*.pdf'],
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'}

# context_data ; données locales et url base en graphe
context_data = {
    'idx_path_pattern': 'auxdir/A*.idx',
    'description': {
        'path_pattern': 'E*.tex',
        'tags': ['%<dscrpt>', '</dscrpt>']
        }
}

# dp pour dépôt
dp_data = {'nom': 'math-pbs',
           'relative_path': '../math-pbs/',
           'execloc_module': execloc_module,
           'execloc_data': execloc_data,
           'publish_data': publish_data,
           'context_data': context_data}

#       paramètres de connexion à l'espace (de publication web)
sp_connect_data = {'region_name': 'fra1',
                   'endpoint_url': 'https://fra1.digitaloceanspaces.com',
                   'bucket': 'maquisdoc-math',
                   'prefix': 'maths-pbs/',
                   'mathPbs_key': 'DO00XUCXPTZGPNNVDW7W',
                   'secret': '+u8PpUIAlnsnTXpXImJNeqmqSvOzYGzr2iS+qhMRSO0',
                   'aws_access_key_id': os.getenv('DO_SPACES_KEY'),
                   'aws_secret_access_key': os.getenv('DO_SPACES_SECRET')
                   }
# certains des paramètres du dessus sont inutiles car ~/.aws/credentials prime.
# À METTRE À JOUR

#      paramètres de connexion à la base de données en graphe
bdg_connect_data = {'URI': os.getenv('NEO4J_URL'),
                    'user': os.getenv('NEO4J_USERNAME'),
                    'password': os.getenv('NEO4J_PASSWORD')}


# paramètres de la maintenance
para = {'depot': dp_data,
        'espace': sp_connect_data,
        'bdg': bdg_connect_data}
"""

# Nouvelle organisation
execloc = {
    'relative_path': '../math-pbs/',
    'modulespec': 'exl_mathPbs',
    'commandes': [
        {'ext': '.tex',
         'patterns': ['A*.tex'],
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
          'imgext':'.pdf',
          'command': [
              "asy",
              "-f",
              "pdf"
              ]
          },
          {'ext': '.py',
           'patterns': ['*_fig.py'],
           'imgdir': '', 'imgext': '.pdf',
           'command': ["python3"]},
          ],
    'publish_data': {
        'patterns': ['pdfdir/A*.pdf'],
        },
    'context_data': {
        'idx_path_pattern': 'auxdir/A*.idx',
        'description': {
            'path_pattern': 'E*.tex',
            'tags': ['%<dscrpt>', '</dscrpt>']
            }
        }
    }
"""
Dictionnaire présentant les paramètres de traitement local des sources.
"""

espace = {
    'credentials': {
        'region_name': 'fra1',
        'endpoint_url': 'https://fra1.digitaloceanspaces.com',
        'bucket': 'maquisdoc-math',
        'prefix': 'maths-pbs/',
                   },
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'
    }
"""
Dictionnaire présentant les paramètres du serveur de publication.
"""

context = {
    'credentials': {
        'URI': os.getenv('NEO4J_URL'),
        'user': os.getenv('NEO4J_USERNAME'),
        'password': os.getenv('NEO4J_PASSWORD')
        },
    'modulespec': 'bdg_mathPbs'
    }
"""
Dictionnaire présentant les paramètres du serveur de contextualisation.
"""

data = {'nom': 'math-pbs',
        'execloc': execloc,
        'espace': espace,
        'context': context}
"""
Dictionnaire présentant tous les paramètres du dépôt.
"""
