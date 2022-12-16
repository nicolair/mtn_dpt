#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Dec  7 06:25:32 2022

@author: remy

Script de maintenance du dépôt `math-pbs` de Git.

  - importe `init_mathPbs` qui code le *manifeste* du dépôt.
  - instancie une classe Depôt ce qui effectue la maintenance
  - affiche le journal de la maintenance

Le nom du sous-dossier de `maquisdoc-depots` est aussi `math-pbs`
sur la machine de travail de l'auteur.
En python, les noms de modules ne doivent pas contenir de "-".
Les modules importés sont donc 'init_mathPbs' et 'exl_mathPbs'
dans lesquels `math-pbs` a été changé en `mathPbs`.

Le manifeste d'un dépôt est la description des conventions d'organisation
d'un dépôt.

Manifeste de `maths-pbs`
========================

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

"""
import init_mathPbs as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    #                        INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.para)
    journal = dp.log

    print(journal)
