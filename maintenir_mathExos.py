#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:51:48 2020

@author: remy

Script de maintenance du dépôt `math-exos` de Git.

  - importe `init_mathExos` qui code le *manifeste* du dépôt.
  - instancie une classe Depôt ce qui effectue la maintenance
  - affiche le journal de la maintenance

Le nom du sous-dossier de `maquisdoc-depots` est aussi `math-exos`
sur la machine de travail de l'auteur.
En python, les noms de modules ne doivent pas contenir de "-".
Les modules importés sont donc 'init_mathExos' et 'exl_mathExos'
dans lesquels `math-exos` a été changé en `mathExos`.

Le manifeste d'un dépôt est la description des conventions d'organisation
d'un dépôt.

Manifeste de `maths-exos`
========================

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
Ils sont mis à jour par ce script de maintenance compilés en pdf,
ces pdf sont placés dans *l'espace*.


Un fichier Latex dont le nom commence par `Aexo_` suivi du code d'un thème
et de 2 chiffres est associé à un un exercice particulier.
Ces fichiers ne devraient pas être édités à la main.
Ils sont mis à jour par ce script de maintenance.
Ces fichiers sont compilés en html, ces html sont placés dans *l'espace*.


"""
import init_mathExos as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    #                        INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.para)
    journal = dp.log

    print(journal)
