#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 20:09:28 2018

@author: remy

Outils d'analyse de fichiers tex
"""
import os


def get_date_srce(nom):
    """
    Renvoie une date de source.

    Fonction récursive.
        Si le fichier ne contient ni input ni includegraphics,
            renvoie la date de maj du fichier.
        Sinon
            renvoie la date la plus récente entre sa date de maj et celle
            des input et includegraphics.
    """
    try:
        date_srce = os.path.getmtime(nom)
    except FileNotFoundError:
        print(nom, ' pas trouvé')
        date_srce = 0

    # date des sources tex inputtés
    liste = get_liste_inputs(nom)
    for fic in liste:
        t = get_date_srce(fic)
        # print(fic,t)
        if t > date_srce:
            date_srce = t

    # date des figures et des lignes de code incluses
    liste = get_liste_includegraphics(nom) + get_liste_lstinputlistings(nom)
    for fic in liste:
        try:
            t = os.path.getmtime(fic)
        except FileNotFoundError:
            print('Erreur : ', fic, ' pas trouvé')
            t = 0
        # print(fic, t)
        if t > date_srce:
            date_srce = t
    return date_srce


def get_liste_inputs(nom):
    """Renvoie la liste des sources tex dans des input."""
    fifi = open(nom, 'r')

    text = fifi.read()
    long = len(text)
    inputs = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\input{', cc, long)
        if c != -1:
            c += 7
            cc = text.find('}', c, long)
            nominput = text[c:cc]
            if '.' not in nominput:
                nominput += '.tex'
            if nominput not in inputs:
                inputs.append(nominput)
    return inputs


def get_liste_includegraphics(nom):
    """Renvoie la liste des figures (pdf) dans des includegraphics."""
    fifi = open(nom, 'r')
    text = fifi.read()
    long = len(text)
    includes = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\includegraphics', cc, long)
        if c != -1:
            # il peut y avoir une option '[width= ]'
            c = text.find('{', c, long)
            c += 1
            cc = text.find('}', c, long)
            fig = text[c:cc]
            # si pas d'extension on place .pdf
            if not os.path.splitext(fig)[1]:
                print('extension pdf manque dans', nom)
                fig += '.pdf'
            if fig not in includes:
                includes.append(fig)
    return includes


def get_liste_lstinputlistings(nom):
    """
    Renvoie une liste des fichiers.

    Ceux contenant des lignes de codes insérées par lstinputlisting
    """
    fifi = open(nom, 'r')
    text = fifi.read()
    long = len(text)
    lstinputs = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\lstinputlisting', cc, long)
        if c != -1:
            # il y a une option '[width= ] à sauter'
            c = text.find('{', c, long)
            c += 1
            cc = text.find('}', c, long)
            lstinput = text[c:cc]
            # si pas d'extension on place .py
            if not os.path.splitext(lstinput)[1]:
                print('extension pdf manque dans', nom)
                lstinput += '.py'
            if lstinput not in lstinputs:
                lstinputs.append(lstinput)
    return lstinputs


def aexec(src):
    """Renvoie vrai si un input plus récent que pdf."""
    ext = os.path.splitext(src)[1]
    img = src.replace(ext, '.pdf')
    # print(img)
    date_img = 0
    date_src = get_date_srce(src)
    if os.path.exists(img):
        date_img = os.path.getmtime(img)
    return date_src > date_img


def acompiler(src, img):
    """
    Renvoie Vrai si src est à compiler.

    Cad si un input de la source est plus récent que l'image

    Parameters
    ----------
    src : TYPE
        DESCRIPTION.
    img : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # imgext = os.path.splitext(img)[1]
    # print(img)
    date_img = 0
    date_src = get_date_srce(src)
    if os.path.exists(img):
        date_img = os.path.getmtime(img)
        # if imgext == '.html':
        #    print(img, date_src > date_img)

    return date_src > date_img
