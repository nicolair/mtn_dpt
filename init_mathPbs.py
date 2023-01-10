"""
Définit les paramètres d'initialisation de la maintenance du dépôt `math-pbs`.

Modifié le 07/01/23 @author: remy

- Code le *manifeste* du dépôt.
- Définit les noms des sous-modules spécifiques
- Définit les accès
    - aux espaces (publication)
    - à la base de données en graphe (contextualisation)

Manifeste du dépôt math-pbs.
--------------------------

Le manifeste d'un dépôt code
- les conventions de nommage des fichiers régissant sa structure
- les commandes de traitement s'appliquant aux fichiers.

Le manifeste d'un dépôt est la description des conventions d'organisation
d'un dépôt.

Un problème est caractérisé par une chaîne de caractère (son titre) qui évoque
vagument son thème.

Le nom des fichiers LateX d'un problème est formé à partir de son titre
    - précédé par `E` pour un énoncé et `C` pour un corrigé
    - précédé par `A` pour le fichier à compiler en pdf du problème corrigé

Exemple `alglin15` est le titre d'un problème d'algèbre linéaire.
L'énoncé est `Ealglin15.tex`, le corrigé est `Calglin15.tex`.
Le fichier à compiler présentant le problème corrigé est `Aalglin15.tex`.

Énoncés ou corrigés peuvent utiliser des fichiers annexes (figures, codes,..)
dont le nom est obtenu en ajoutant `_numéro` à la fin avant l'extension.

Exemple `p3impko` est le titre d'un problème portant sur le thème
"période 3 implique chaos". Le corrigé comporte une figure `Cp3impko_1.pdf`
formée à partir de la source `Cp3impko_1.asy` écrit en `asymptote` langage
de création de figure compilé en pdf. L'énoncé comporte aussi une figure
`Ep3impko_1.pdf` formée à partir de `Ep3impko_1.asy`

Un fichier dont le nom est `Atitre.tex` ne devrait pas être édité à la main.
Ils sont formés et mis à jour par ce script de maintenance.

Les fichiers `Atitre.tex` sont compilés en pdf placés dans `pdfdir`,
puis téléchargés dans *l'espace*.

Paramètres d'accès
------------------
Ce sous-module ne définit que les paramètres publics. Les paramètres secrets
sont définis par
- variables d'environnement `NEO4J_URL`, `NEO4J_PASSWORD`
 pour la base de données'
- le fichier `~/.aws` pour l'espace de publication.

"""

import os

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

# module spécifique
execloc_module = 'exl_mathPbs'

# publish_data : fichiers à publier
publish_data = {
    'patterns': ['pdfdir/A*.pdf'],
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'}

# dp pour dépôt
dp_data = {'nom': 'math-pbs',
           'relative_path': '../math-pbs/',
           'execloc_module': execloc_module,
           'execloc_data': execloc_data,
           'publish_data': publish_data}


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

#      paramètres de connexion à la base de données en graphe
bdg_connect_data = {}
# ###########   FIN DE ZONE SECRETE    ###################


# paramètres de la maintenance
para = {'depot': dp_data, 'espace': sp_connect_data, 'bdg': bdg_connect_data}
