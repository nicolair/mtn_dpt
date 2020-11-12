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
        Fonction récursive. 
        Si un fichier ne contient ni input ni includegraphics renvoie 
            la date de maj du fichier.
        Sinon renvoie la date la plus récente entre sa date de maj et celle
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
        #print(fic,t)
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
        #print(fic, t)
        if t > date_srce:
            date_srce = t
    return date_srce

def get_liste_inputs(nom):
    """
    Liste des sources tex dans des input.
    """
    fifi = open(nom,'r')
        
    text = fifi.read()
    l = len(text)
    inputs = [] 
    c , cc = 0 , 0 #compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\input{',cc,l)
        if c!= -1:
            c += 7
            cc = text.find('}', c ,l)
            nominput = text[c:cc]
            if '.' not in nominput :
                nominput += '.tex'
            if not nominput in inputs:
                inputs.append(nominput)
    return inputs
        
def get_liste_includegraphics(nom):
    """
    Liste des figures (pdf) dans des includegraphics.
    """
    fifi = open(nom,'r')
    text = fifi.read()
    l = len(text)
    includes = [] 
    c , cc = 0 , 0 #compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\includegraphics',cc,l)
        if c!= -1:
            # il peut y avoir une option '[width= ]'
            c = text.find('{',c,l)
            c += 1
            cc = text.find('}', c ,l)
            fig = text[c:cc]
            # si pas d'extension on place .pdf
            if not os.path.splitext(fig)[1]:
                print('extension pdf manque dans',nom)
                fig += '.pdf'
            if not fig in includes:
                includes.append(fig)
    return includes
        
def get_liste_lstinputlistings(nom):
    """
    Liste des fichiers contenant des lignes de codes
        insérées par lstinputlisting
    """
    fifi = open(nom,'r')
    text = fifi.read()
    l = len(text)
    lstinputs = [] 
    c , cc = 0 , 0 #compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\lstinputlisting',cc,l)
        if c!= -1:
            # il y a une option '[width= ] à sauter'
            c = text.find('{',c,l)
            c += 1
            cc = text.find('}', c ,l)
            lstinput = text[c:cc]
            # si pas d'extension on place .py
            if not os.path.splitext(lstinput)[1]:
                print('extension pdf manque dans', nom)
                lstinput += '.py'
            if not lstinput in lstinputs:
                lstinputs.append(lstinput)
    return lstinputs

def aexec(src):
    """renvoie vrai si un input plus récent que pdf"""
    ext = os.path.splitext(src)[1]
    img = src.replace(ext,'.pdf')
    #print(img)
    date_img = 0
    date_src = get_date_srce(src)
    if os.path.exists(img):
        date_img = os.path.getmtime(img)
    return date_src > date_img
