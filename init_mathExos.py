# -*- coding: utf-8 -*-
"""
Ce module code et présente le *manifeste* du dépôt `math-exos`.

Modifié le 04/03/23 @author: remy

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

L'élément essentiel de ce dépôt est un exercice. Un exercice particulier est caractérisé par une chaîne (appelé ici assez improprement son titre) formée de 2 lettres puis de 2 chiffres.

Les 2 lettres codent un thème d'exercice, les 2 chiffres codent le numéro de l'exercice dans le thème.

Le fichier [`_codes.csv`](https://github.com/nicolair/math-exos/blob/master/_codes.csv) dans le dépôt contient la liste des codes avec une
brève description. Les premières lignes sont reproduites au dessous :

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

Les noms des fichiers LateX caractérisant un exercice est formé à partir de son titre: précédé par `E` pour l'énoncé et par `C` pour le corrigé. Parfois l'exercice n'est pas encore corrigé et le fichier `C` n'existe pas. Un auteur travaille essentiellement dans ces fichiers `E` et `C`.

Exemple `Ecp03.tex` et `Ccp03.tex` pour l'exercice numéro 3 portant sur les
nombres complexes.

Un fichier Latex dont le nom commence par `Aexo_` suivi du titre d'un exercice présente un exercice (éventuellement corrigé) particulier. De tels fichiers ne devraient pas être édités à la main. Ils sont mis à jour par la maintenance puis compilés dans des fichiers html placés dans *l'espace* de publication.
 
Un fichier Latex dont le nom commence par `A` suivi du code d'un thème (sans numéro) est la *feuille d'exercice* sur le thème codé qui rassemble tous les exercices du thème. De tels fichiers ne devraient pas être édités à la main.
Ils sont mis à jour par la maintenance puis compilés dans des fichiers pdf placés dans *l'espace* de publication.

### Traitement local

- Avant publication

- Avant contextualisation

### Publication

Voir le sous-module [`espace`](espace.html) pour la mis en oeuvre de la publication. 

Ce sous-module ne définit en clair que les paramètres publics du serveur de publication.
Les credentials secrets sont définis dans le fichier local `~/.aws`.


### Contextualisation

Voir les sous modules [`graphdb`](graphdb.html), [`bdg_mathExos`](bdg_mathExos.html) pour la mise en oeuvre de la contextualisation.

Ce sous-module ne définit en clair que les paramètres publics du serveur de contextualisation.
Les credentials secrets sont définis dans les variables d'environnement `NEO4J_URL` et `NEO4J_PASSWORD`.

"""
import os

# nouvelle organisation

execloc = {
    'relative_path': '../math-exos/',
    'modulespec': 'exl_mathExos',
    'commandes': [
        {'ext': '.tex',
         'patterns': ['A_*.tex'],
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
          {'ext': '.tex',
           'patterns': ['Aexo_*.tex'],
           'imgdir': 'htmldir/',
           'imgext': '.html',
           'command': [
               'make4ht',
               '-u',
               '-d',
               'htmldir'
               ]
           }
        ],
    'publish_data': {
        'patterns': ['pdfdir/A_*.pdf', 'htmldir/*']
        },
    'context_data': {
        }
    }

espace = {
    'credentials': {
        'region_name': 'fra1',
        'endpoint_url': 'https://fra1.digitaloceanspaces.com',
        'bucket': 'maquisdoc-math',
        'prefix': 'maths-exos/',
                   },
        'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'
    }

context = {
    'credentials': {
        'URI': os.getenv('NEO4J_URL'),
        'user': os.getenv('NEO4J_USERNAME'),
        'password': os.getenv('NEO4J_PASSWORD')
        },
    'modulespec': 'bdg_mathExos'
    }

manifeste = {'nom': 'math-exos',
             'execloc': execloc,
             'espace': espace,
             'context': context}



