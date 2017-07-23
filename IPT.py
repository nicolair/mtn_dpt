# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:49:49 2017

@author: remy
"""
import maintenir, os
nom_depot = 'IPT'

"""
types de fichiers
"""
type_fic = {}
type_fic['cours'] = maintenir.Type('src tex doc de cours','*.cours.doc.tex','.tex')
type_fic['A'] = maintenir.Type('src tex doc de type A','A*.doc.tex','.tex')
type_fic['TP'] = maintenir.Type('src tex doc de type TP','TP*.doc.tex','.tex')
type_fic['S'] = maintenir.Type('src tex doc de type DS','S*doc.tex','.tex')
type_fic['exo'] = maintenir.Type("src tex doc de type exo",'exo_*_A.doc.tex','.tex')
type_fic['figasy'] = maintenir.Type("fichiers asy sources de figures",'*_fig.asy','.asy')
type_fic['figpy'] = maintenir.Type("fichiers python sources de figures",'*_fig.py','.asy')
type_fic['tex'] = maintenir.Type("fichiers tex",'*.tex','.tex')


print("\n ##############################################################")
print('\t \t maintenance du dépôt IPT')
print('\t \t ######################## \n')
depot_path = '../' + nom_depot
diffusion_path = maintenir.diffusion_path + nom_depot + "/"

#print(depot_path,diffusion_path)
os.chdir(depot_path)

"""
Exécution des scripts de figure
"""
for key in ['figasy','figpy']:
    type_scrpt = type_fic[key]
    print('\n #############', type_scrpt.comm)
    lili = type_scrpt.chercher_scripts()
    #print(lili)
    for fifi in lili:
        #print(fifi)
        scrpt = maintenir.Script(fifi)
        if scrpt.a_exec:
            scrpt.executer()
            print(scrpt.nom, scrpt.nom_pdf)

"""
Exécution des scripts de documents
"""
for key in ['A','TP','S','exo','cours']:
    type_scrpt = type_fic[key]
    print('\n #############', type_scrpt.comm)
    lili = type_scrpt.chercher_scripts()
    for fifi in lili:
        scrpt = maintenir.ScriptTex(fifi)
        #if scrpt.lstinputlistings:
            #pass
            #print(scrpt.nom,scrpt.lstinputlistings)
        if scrpt.a_exec:
            #pass
            scrpt.executer()
            scrpt.diffuser(nom_depot)
            print(scrpt.nom, scrpt.commande)

os.chdir('../maintenance')