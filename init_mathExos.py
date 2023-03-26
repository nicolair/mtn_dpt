# -*- coding: utf-8 -*-
"""
Ce module code et présente le *manifeste* du dépôt `math-exos`.

Modifié le 09/03/23 @author: remy

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

Les noms des fichiers LateX caractérisant un exercice sont formés à partir de son titre: précédé par `E` pour l'énoncé et par `C` pour le corrigé. Parfois l'exercice n'est pas encore corrigé et le fichier `C` n'existe pas. Un auteur travaille essentiellement dans ces fichiers `E` et `C`.

Exemple `Ecp03.tex` et `Ccp03.tex` pour l'exercice numéro 3 portant sur les
nombres complexes.

Un fichier Latex dont le nom commence par `Aexo_` suivi du titre d'un exercice présente un exercice (éventuellement corrigé) particulier. De tels fichiers ne devraient pas être édités à la main. Ils sont mis à jour par la maintenance puis compilés dans des fichiers html placés dans *l'espace* de publication.
 
Un fichier Latex dont le nom commence par `A` suivi du code d'un thème (sans numéro) est la *feuille d'exercice* sur le thème codé qui rassemble tous les exercices du thème. De tels fichiers ne devraient pas être édités à la main.
Ils sont mis à jour par la maintenance puis compilés dans des fichiers pdf placés dans *l'espace* de publication.

### Traitement local

- Avant compilation
    - mise à jour des fichiers LateX d'exercices individuels `Aexo_`
    - mise à jour des fichiers Latex de feuille par thème `A`
    
- Avant contextualisation

- Compilation

- Avant publication

### Publication

Voir le sous-module [`espace`](espace.html) pour la mis en oeuvre de la publication. 

Ce sous-module ne définit en clair que les paramètres publics du serveur de publication.
Les credentials secrets sont définis dans le fichier local `~/.aws`.


### Contextualisation

#### Noeuds

Les noeuds attachés au dépôt d'exercices sont de plusieurs types. Pour chaque type, on indique un exemple de requête cypher renvoyant un unique noeud.

- Noeud (`Document`) associé à un exercice particulier caractérisé par son titre
    
        MATCH (e:Document {typeDoc:"exercice", discipline:"mathématique", titre:"dt23"}) RETURN e

- Noeud (`Document`) associé à une feuille d'exercices caractérisée par son titre
    
        MATCH (f:Document {typeDoc:"liste exercices", titre:"Déterminants"}) RETURN f

- Noeud (`Concept`) associé à un thème d'exercices caractérisé par son littéral
    
        MATCH (c:Concept {typeConcept:"thème feuille exercices", :"Déterminants"}) RETURN c

Le titre du document "feuille" est égal au littéral du concept "thème" associé au même thème d'exercices.
#### Arêtes

- Arête (`CONTIENT`) entre une feuille et un exercice
- Arête (`EVALUE`) entre un exercice et le concept de son thème
- Arête (`EVALUE`) entre une feuille et le concept de son thème
- Arête (`INDEXE`) entre un exercice et un concept dont le littéral est indéxé
 "en dur" dans le fichier source Latex de l'exercice.

Le titre du document "feuille" et le littéral du concept évalué attaché à la même ligne du fichier `_code.csv` doivent être égaux.

On peut insérer directement dans la base des relations qui ne viennent pas des fichiers du dépot. Par exemple des relations `EVALUE` entre un concept (autre qu'un thème d'exercice) et un exercice spécifique.

Voir les sous modules [`graphdb`](graphdb.html), [`bdg_mathExos`](bdg_mathExos.html) pour la mise en oeuvre de la contextualisation.

Ce sous-module ne définit en clair que les paramètres publics du serveur de contextualisation.
Les credentials secrets sont définis dans les variables d'environnement `NEO4J_URL` et `NEO4J_PASSWORD`.

### Scénarios de travail admissibles
- supprimer un exercice
- créer un exercice
- ajouter un corrigé
- modifier un énoncé ou un corrigé
- ajouter un index en insérant à la main
    - les commandes `index{}` dans le fichier `E`
    - la commande `\makeindex` dans le préambile du fichier `Aexo`

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
        'idx_path_pattern': 'Aexo_*.idx'
        }
    }

espace = {
    'credentials': {
        'region_name': 'fra1',
        'endpoint_url': 'https://fra1.digitaloceanspaces.com',
        'bucket': 'maquisdoc-math',
        'prefix': 'math-exos/',
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



