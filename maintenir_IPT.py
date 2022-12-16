#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script maintenir_IPT de maintenance du dépôt IPT
"""
#le nom du dépôt effectif intervient seulement dans la première ligne

###########             IMPORTATIONS

#import glob #, fnmatch, subprocess, shutil #, glob os

#importe le module de paramètres spécifiques
import init_IPT as init_DPT
import depot, execlocal, espace #, bdgraph
journal = {}

para = init_DPT.para
dp_data = para['depot']

#                        INSTANCIATION d'un objet Depot
dp = depot.Depot(para['depot'])

#####               INSTANCIATIONS DES INTERFACES  #############

# objet Execlocal (pour la compilation) 
#aexecuter_data = dp.aexecuter()
aexecuter_data = dp.aexecuter()
exl = execlocal.Execlocal(aexecuter_data)

# objet Espace (pour la publication)
apublier_data = dp.apublierImg()
esp = espace.Espace(para['espace'],apublier_data)

# objet Bdgraph (pour la contextualisation)
#modif du 27/01/19 ne marche plus
#acontextualiser_data = dp.acontextualiser()
#bdg = bdgraph.Bdgraph(para['bdg'],acontextualiser_data)

#####                MISES A JOUR   ###########
# images et documents locaux
journal['exl'] = exl.MAJ()

# espace distant de publication des images
journal['esp'] = esp.MAJ()

# base de données en graphe 
#journal['bdg'] = bdg.MAJ()

#                        Journaux à afficher

# instanciation du dépôt
#print(dp.log)

#compilation
#print(jrnl_compil)

# MAJ de l'espace
#print(jrnl_esp['supprimer'])
#print(jrnl_esp['placer'])
#print(jrnl_autoriser)
