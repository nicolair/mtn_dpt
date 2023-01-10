# -*- coding: utf-8 -*-
"""
Définit les paramètres d'initialisation de la maintenance du dépôt `math-exos`.

Modifié le 07/01/23 @author: remy

- Code le *manifeste* du dépôt.
- Définit les noms des sous-modules spécifiques
- Définit les accès
    - aux espaces (publication)
    - à la base de données en graphe (contextualisation)

Manifeste de `maths-exos`
----------------------

Le manifeste d'un dépôt code
- les conventions de nommage des fichiers régissant sa structure
- les commandes de traitement s'appliquant aux fichiers.

Un code de 2 lettres caractérise un thème d'exercice.
Le fichier `_codes.csv` dans le dépôt contient la liste des codes avec une
brève description. Les premières lignes sont reproduites au dessous ::

    codetheme;description
    al;groupes anneaux corps
    am;avec maple
    ao;automorphismes orthogonaux
    ap;approximations (zéros, intégrales, nombres réels)
    ar;arithmétique dans Z et K[X]
    ce;(courbes euclidiennes) étude métrique des courbes
    cg;Fonctions d’une Variable Géométrique : continuité
    co;coniques
    cp;nombres complexes

Le nom du fichier LateX d'un exercice est formé à partir du code de son thème
    - précédé par `E` pour un énoncé et `C` pour un corrigé
    - suivi du numéro (codé sur 2 chiffres) de l'exercice dans le thème

Exemple `Ecp03.tex` et `Ccp03.tex` pour l'exercice numéro 3 portant sur les
nombres complexes.

Un fichier Latex dont le nom commence par `A` suivi du code d'un thème'
est une *feuille d'exercice* sur le thème codé .
Ces fichiers ne devraient pas être édités à la main.
Ils sont mis à jour par ce script de maintenance puis compilés en pdf.
Ces pdf sont placés dans *l'espace* de publication.


Un fichier Latex dont le nom commence par `Aexo_` suivi du code d'un thème
et de 2 chiffres est associé à un un exercice particulier.
Ces fichiers ne devraient pas être édités à la main.
Ils sont mis à jour par ce script de maintenance.
Ces fichiers sont compilés en html, ces html sont placés dans *l'espace* de
 publication.

Paramètres d'accès
------------------
Ce sous-module ne définit que les paramètres publics. Les paramètres secrets
sont définis par
- variables d'environnement `NEO4J_URL`, `NEO4J_PASSWORD`
 pour la base de données'
- le fichier `~/.aws` pour l'espace de publication.

"""

#  paramètres du dépôt
# fichiers à exécuter localement
execloc_data = [
    {'ext': '.tex', 'patterns': ['A_*.tex'],
     'imgdir': 'pdfdir/', 'imgext': '.pdf',
     'command': ["latexmk", "-pdf", "-emulate-aux-dir",
                 "-auxdir=auxdir", "-outdir=pdfdir"]},
    {'ext': '.asy', 'patterns': ['*_fig.asy'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["asy", "-f", "pdf"]},
    {'ext': '.py', 'patterns': ['*_fig.py'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["python3"]},
    {'ext': '.tex', 'patterns': ['Aexo_*.tex'],
     'imgdir': 'htmldir/', 'imgext': '.html',
     'command': ['make4ht', '-u', '-d', 'htmldir']}
    ]

# module spécifique
execloc_module = 'exl_mathExos'

# publish_data : fichiers à publier
publish_data = {
    'patterns': ['pdfdir/A_*.pdf', 'htmldir/*'],
    # 'liste': ['A_'],
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'}

# dp pour dépôt
dp_data = {'nom': 'math-exos',
           'relative_path': '../math-exos/',
           'execloc_module': execloc_module,
           'execloc_data': execloc_data,
           'publish_data': publish_data}


# Paramètres d'accès
#       paramètres de connexion à l'espace (de publication web)
sp_connect_data = {'region_name': 'fra1',
                   'endpoint_url': 'https://fra1.digitaloceanspaces.com',
                   'bucket': 'maquisdoc-math',
                   'prefix': 'math-exos/'}
#      paramètres de connexion à la base de données en graphe
# local
# bdg_data = {'url' : 'bolt://localhost:7687', 'user': "neo4j", 'pw':"3128"}
# graphenedb
bdg_connect_data = {}
# bdg_connect_data = {
#    'uri' : "bolt://hobby-emmpngdpepmbgbkeiodbecbl.dbs.graphenedb.com:24786",
#    'user': "mimi", 'pw': "b.qzcs8g8XgxeB.Sbc5iAoGjwGi60fr"}
# ###########   FIN DE ZONE SECRETE    ###################


# paramètres de la maintenance
para = {'depot': dp_data, 'espace': sp_connect_data, 'bdg': bdg_connect_data}
