#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de scripts (à exécuter localement) spécifiques au dépôt d'exercices et complétant les commandes définies dans le manifeste..

Modifié le 09/02/23 @author: remy

La fonction `exec()` exécute les tâches spécifiques complémentaires. Elle est appelée lors de l'instanciation de la classe `Execlocal`.

"""
import csv
import glob
import os.path
import re
import scantex


dp_data = {}
dp_data['relative_path'] = '../math-exos/'
relpath = '../math-exos/'
lineprefix = "\n \t \t"


def exec():
    """
    Forme les exos individuels et les feuilles d'exos LateX.

    - Lit les thèmes depuis le fichier `_codes.csv`
    - Pour chaque thème, forme le fichier LateX `A_`
    - Pour chaque exercice, forme le fichier LateX `Aexo_`
    - Renvoie un journal de l'exécution


    Returns
    -------
    log : TYPE str
        DESCRIPTION journal de l'exécution des scripts.

    """
    log = lineprefix + 'Scripts du module spécifique (fonction exec())'

    # Feuilles par thèmes
    theme = getThemes()
    log += '\n \t\t\t Création modification des feuilles LateX'
    for code in theme:
        if aecrirefeuilleA(code):
            log += ecritFeuilleA(code, theme[code])

    # Exercices individuels "Aexo_"
    log += '\n\n \t \t \t Création modification des "Aexo_" Latex individuels'
    lili = listeExos()
    for theme in lili:
        for nomexo in lili[theme]:
            if aecrireAexo(nomexo):
                log += ecritAexo(nomexo)

    return log


def ecritFeuilleA(code, dscrpt):
    """
    Exécute les scripts Python spécifiques à ce dépôt.

     ici
        - création ou maj feuille d'exos Latex d'un thème


    Parameters
    ----------
    code : TYPE str
        DESCRIPTION code du thème dans le fichier `_code.csv`.
    dscrpt : TYPE str
        DESCRIPTION description du thème dans le fichier `_code.csv`.

    Returns
    -------
    log : TYPE str
        DESCRIPTION journal de l'exécution.

    """
    log = '\n \t \t \t' + code + ' : ' + dscrpt
    exos_list = glob.glob(relpath + 'E' + code + '*.tex')
    exos_list.sort()
    dates = map(os.path.getmtime, exos_list)
    date_inputs = max(dates)

    # début fichier
    Latex = '\\input{exopdf} \n'
    Latex += '\\begin{document} \n'

    # énoncés
    Latex += '\\chead{ ' + dscrpt + ': énoncés.}\n'
    Latex += '\\begin{enumerate}\n'
    for exo in exos_list:
        exo = os.path.basename(exo)
        Latex += '  \\item \\input{' + exo + '} \n'
    Latex += '\\end{enumerate} \n'

    # corrigés
    Latex += '\\clearpage \n'
    Latex += '\\chead{' + dscrpt + ': corrigés.}\n'
    Latex += '\\begin{enumerate}\n'
    for exo in exos_list:
        exoC = exo.replace('E' + code, 'C' + code)
        if os.path.isfile(exoC):
            date_inputs = max(date_inputs, os.path.getmtime(exoC))
            Latex += '  \\item \\input{' + os.path.basename(exoC) + '} \n'
        else:
            Latex += '  \\item ' + os.path.basename(exoC) + ' manque. \n'
    Latex += '\\end{enumerate} \n'

    # fin fichier
    Latex += '\\end{document}'

    # écrit le Latex dans un fichier A#
    pathA = relpath + 'A_' + code + '.tex'

    with open(pathA, 'w') as fifi:
        fifi.write(Latex)
        log += ' NOUVEAU OU MODIFIÉ ' + pathA

    return log


def aecrirefeuilleA(code):
    """
    Renvoie VRAI ou FAUX.

    VRAI si le fichier LateX "A" du thème doit être créé ou modifié
    c'est à dire si
        - le fichier "A" n'existe pas
        ou
        - la liste des fichiers "E" ou "C" n'est pas dans celle des input

    Parameters
    ----------
    code : TYPE str
        DESCRIPTION code du theme.

    Returns
    -------
    bool.

    """
    pathA = relpath + 'A_' + code + '.tex'

    bouboule = False
    if not os.path.isfile(pathA):
        bouboule = True
    else:
        inputs = set(scantex.get_liste_inputs(pathA))
        fifi = set(listeExos()[code]) | set(listeCorriges()[code])
        bouboule = not (fifi <= inputs)
    return bouboule


def aecrireAexo(nomexo):
    """
    Renvoie VRAI si le fichier "Aexo" de l'exercice doit être créé
    ou modifié. C'est à dire si :
        - le fichier "Aexo_" n'existe pas'
        ou
        - le fichier "Aexo_" ne contient pas de corrigé alors qu'il existe
        un fichier "C".
    Parameters
    ----------
    nomexo : TYPE str
        DESCRIPTION nom du fichier "E" d'un exercice.

    Returns
    -------
    TYPE bool

    """
    exospath = dp_data['relative_path']
    nomexoC = nomexo.replace('E', 'C')
    nomexoA = nomexo.replace('E', 'Aexo_')
    pathC = exospath + nomexoC
    pathA = exospath + nomexoA
    bouboule = False
    if not os.path.isfile(pathA):
        bouboule = True
    elif os.path.isfile(pathC):
        with open(pathA) as fifi:
            latex = fifi.read()
            if "pas encore de corrigé" in latex:
                bouboule = True
    return bouboule


def ecritAexo(nomexo):
    """
    Forme le fichier latex "Aexo_" d'un exercice particulier'
    et l'écrit dans le dépôt.


    Parameters
    ----------
    nomexo :
        TYPE str
        DESCRIPTION  nom du fichier de l'exercice (énoncé).

    Returns
    -------
    None ou le nom du fichier Aexo modifié.

    """
    log = ''
    exospath = dp_data['relative_path']
    nomexoE = nomexo
    nomexoC = nomexo.replace('E', 'C')
    nomexoA = nomexo.replace('E', 'Aexo_')
    pathE = exospath + nomexoE
    pathC = exospath + nomexoC
    pathA = exospath + nomexoA

    # début fichier
    Latex = '\\input{exo4ht} \n'
    Latex += '\\begin{document} \n'
    Latex += 'Énoncé \n\n'
    Latex += '\\input{' + os.path.basename(pathE) + '}\n\n'
    Latex += 'Corrigé \n\n'
    if os.path.isfile(pathC):
        Latex += '\\input{' + os.path.basename(pathC) + '}\n'
    else:
        Latex += 'pas encore de corrigé\n'
    Latex += '\\end{document}'
    # print(Latex)

    """
    On écrit toujours.
    """
    with open(pathA, 'w') as fifi:
        fifi.write(Latex)
        log += '\n \t\t\t' + os.path.basename(pathA)
    return log
    # sinon ne renvoie rien


def listeExosTheme(code):
    """
    Renvoie la liste des exos du theme codé

    Parameters
    ----------
    code:
        TYPE str
        DESCRIPTION le code d'un thème

    Returns
    -------
    liste de chemins de fichier Latex d'énoncé
    """
    exos_list = glob.glob(relpath + 'E' + code + '*.tex')
    exos_list.sort()
    return exos_list


def listeExosCorrTheme(code):
    """
    Renvoie la liste des exos corrigés du theme codé

    Parameters
    ----------
    code:
        TYPE str
        DESCRIPTION le code d'un thème

    Returns
    -------
    liste de chemins de fichiers Latex de corrigés
    """
    exos_list = glob.glob(relpath + 'C' + code + '*.tex')
    exos_list.sort()
    return exos_list


def getThemes():
    """
    Lit les thèmes depuis le fichier _codes.csv

    Returns
    -------
    dictThemes : TYPE dict
        DESCRIPTION key=code, val=description.

    """
    dictThemes = {}
    with open('../math-exos/' + '_codes.csv', newline='') as csvfile:
        riri = csv.reader(csvfile, delimiter=';')
        for row in riri:
            dictThemes[row[0]] = row[1]
        dictThemes.pop('codetheme')
    return dictThemes


def listeExos():
    """

    Returns
    -------
    dictionnaire
        - clé = code d'un thème
        - valeur = liste des noms des fichiers d'énoncé

    """
    themes = getThemes()
    exospath = relpath
    files = os.listdir(exospath)

    exercices = {}

    for code in themes:
        exercices[code] = []
        regexpr = "^E" + code + "[0-9]{2}.tex"
        for file in files:
            if re.match(regexpr, file):
                exercices[code].append(file)
        exercices[code].sort()
    return exercices


def listeCorriges():
    """

    Returns
    -------
    dictionnaire
        - clé = code d'un thème
        - valeur = liste des noms des fichiers d'énoncé

    """
    themes = getThemes()
    exospath = relpath
    files = os.listdir(exospath)

    exercices = {}

    for code in themes:
        exercices[code] = []
        regexpr = "^C" + code + "[0-9]{2}.tex"
        for file in files:
            if re.match(regexpr, file):
                exercices[code].append(file)
        exercices[code].sort()
    return exercices


def listeExosNoncorr():
    """

    Returns
    -------
    dictionnaire des exercices (énoncés) non corrigés
        - clé = code d'un thème
        - valeur = liste des noms des fichiers d'énoncé


    """
    exospath = relpath
    exercices = listeExos()
    exercicesNC = {}
    for code in exercices:
        exercicesNC[code] = []
        for file in exercices[code]:
            fileC = file.replace('E', 'C')
            pathC = exospath + fileC
            if not os.path.isfile(pathC):
                exercicesNC[code].append(file)
    return exercicesNC


def ecritTousAexos():
    """
    Écrit tous les "Aexos_" dans le dépôt. Ne doit être utilisé qu'une fois

    Returns
    -------
    None.

    """
    exercices = listeExos()
    for code in exercices:
        for nomexo in exercices[code]:
            ecritAexo(nomexo)


def listeAexosNoncorr():
    """
    Liste des enoncés dont le "Aexo_" ne contient pas de corrigé.

    Returns
    -------
    None.

    """
    exospath = relpath
    exercices = listeExos()
    AexosNoncorr = {}
    for code in exercices:
        AexosNoncorr[code] = []
        for nomexo in exercices[code]:
            nomexoA = nomexo.replace('E', 'Aexo_')
            pathA = exospath + nomexoA
            with open(pathA) as fifi:
                latex = fifi.read()
                if "pas encore de corrigé" in latex:
                    AexosNoncorr[code].append(nomexo)
        AexosNoncorr[code].sort()
    return AexosNoncorr


def modifTousAexos():
    """
    Modifie tous les "Aexos" qui doivent l'être.
    C'est à dire ceux qui contiennent "pas encore de corrigé" alors
    qu'un corrigé existe.

    Returns
    -------
    None.

    """
    lA = listeAexosNoncorr()
    lE = listeExosNoncorr()
    lili = []
    for code in lA:
        amodif = set(lA[code]) - set(lE[code])
        for nomexo in amodif:
            print(nomexo)
            ecritAexo(nomexo)
            lili.append(nomexo)
    return lili
