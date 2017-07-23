# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 07:48:13 2017

@author: remy

Module d'outils de maintenance.
"""

import os, fnmatch, subprocess, shutil

class FicTex():
    """ 
    Classe représentant un fichier tex.
    Il n'est pas forcément à exécuter seul, il peut être inclus.
    Il peut aussi inclure des figures ou des lignes de codes.
    """
    def __init__(self,nom):
        self.nom = nom
        #self.nom_pdf = self.nom.replace('.tex','.pdf')
        self.inputs = self.get_liste_inputs()
        self.includegraphics = self.get_liste_includegraphics()
        self.lstinputlistings = self.get_liste_lstinputlistings()
        self.date_srce = self.get_date_srce()

    def get_liste_inputs(self):
        """
        Liste des sources tex dans des input.
        """
        fifi = open(self.nom,'r')
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
                if nominput[-4:] != '.tex':
                    nominput += '.tex'
                if not nominput in inputs:
                    inputs.append(nominput)
        return inputs
        
    def get_liste_includegraphics(self):
        """
        Liste des figures (pdf) dans des includegraphics.
        """
        fifi = open(self.nom,'r')
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
                    print('extension pdf manque dans',self.nom)
                    fig += '.pdf'
                if not fig in includes:
                    includes.append(fig)
        return includes
        
    def get_liste_lstinputlistings(self):
        """
        Liste des fichiers contenant des lignes de codes
            insérées par lstinputlisting
        """
        fifi = open(self.nom,'r')
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
                    print('extension pdf manque dans',self.nom)
                    lstinput += '.py'
                if not lstinput in lstinputs:
                    lstinputs.append(lstinput)
        return lstinputs
        
        

    def get_date_srce(self):
        """
        Fonction récursive. 
        Si un fichier ne contient ni input ni includegrphics renvoie 
            la date de maj du fichier.
        Sinon renvoie la date la plus récente entre sa date de maj et celle
            des input et includegraphics.
        """
        try:
            date_srce = os.path.getmtime(self.nom)
        except FileNotFoundError:
            print(self.nom, ' pas trouvé')
            date_srce = 0
        
        # date des sources tex inputtés
        liste = self.inputs
        for fic in liste:
            srcetex = FicTex(fic) 
            t = srcetex.date_srce 
            #print(fic,t)
            if t > date_srce:
                date_srce = t
                
        # date des figures et des lignes de code incluses
        liste = self.includegraphics + self.get_liste_lstinputlistings()
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

class Script:
    """    
    Classe représentant un script exécutable (tex asy ou py). 
    Il produit un fichier pdf (document ou figure) dont le nom est obtenu
    à partir du nom du script en changeant l'extension en .pdf
    """
    def __init__(self, nom):
        self.nom = nom
        self.suffixe = os.path.splitext(self.nom)[1]
        self.nom_pdf = self.nom.replace(self.suffixe,'.pdf')
        self.commande = self.get_commande()
        self.date_img = self.get_date_img()
        self.date_srce= self.get_date_srce()
        self.a_exec = self.date_img < self.date_srce

    def get_commande(self):
        return commande_list[self.suffixe] + [self.nom]
        
    def get_date_srce(self):
        date = 0
        try:
            date = os.path.getmtime(self.nom)
        except FileNotFoundError :
            print('ERREUR' + self.nom + 'pas trouvé')
        return date
        
    def get_date_img(self):
        date_img = 0.
        if os.path.exists(self.nom_pdf):
            date_img = os.path.getmtime(self.nom_pdf)
        return date_img
        
    def executer(self):
        try :
            subprocess.run(self.commande)
        except subprocess.SubprocessError :
            print('ERREUR exécution de ', self.commande)
        
class ScriptTex(Script,FicTex):
    """
    Classe représentant un script tex produisant un document.
    """
    def __init__(self, nom):
        self.nom = nom
        self.suffixe = ".tex"
        self.nom_pdf = self.nom.replace('.tex','.pdf')
        self.commande = self.get_commande()
        self.date_img = self.get_date_img()
        self.inputs = self.get_liste_inputs()
        self.includegraphics = self.get_liste_includegraphics()
        self.date_srce= FicTex.get_date_srce(self)
        self.lstinputlistings = self.get_liste_lstinputlistings()
        self.a_exec = self.date_img < self.date_srce

    def diffuser(self,dir):
        diff_pdf = diffusion_path + dir + '/' + self.nom_pdf
        print(diff_pdf)
        shutil.copyfile(self.nom_pdf , diff_pdf)
    
class Type:
    """
    Classe représentant un type de script.
    """
    def __init__(self,comm,pattern, suffixe):
        self.comm = comm
        self.pattern = pattern
        self.suffixe = suffixe
        
    def chercher_scripts(self):
        """
        Renvoie la liste des scripts de ce type.
        """
        #print('recherche des scripts', self.comm)
        fics = os.listdir()
        lili = []
        for fic in fics:
            if fnmatch.fnmatchcase(fic,self.pattern):
                lili.append(fic)
        return lili        


diffusion_path = "/var/www/maquisdoc/documents/"

commande_list = {".tex":["latexmk", "-f", "-pdf"] ,
                 ".asy":["asy","-f","pdf"], ".py":["python3"]}


import IPT
        
