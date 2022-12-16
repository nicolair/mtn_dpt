# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 08:56:04 2018

Exécution locale des scripts de maintenance lors de l'instanciation de
la classe `Execlocal`.

@author: remy

"""
import importlib
import subprocess
import glob
import os.path

import scantex


class Execlocal:
    """
    Exécute les scripts de compilation lors de l'instanciation.

    Présente les fichiers publiables dans la propriété 'publiables'

    """

    def __init__(self, depot_data):
        """
        Initialise la classe à compléter.

            récupère les paramètres du dépôt
            initialise la propriété journal (`log`)
            importe le module spécifique au dépôt
            exécute
                - scripts python spécifiques maj fichiers LateX
                - commandes de compilation
        Parameters
        ----------
        depot_data : TYPE dictionnaire
            DESCRIPTION   codage du *manifeste* du dépôt
                exemple pour le dépôt mathExos
                ------------------------------
                  {
                    "nom" : "math-exos",
                    "relative_path" : "../math-exos/",
                    "execloc_module" : "exl_mathExos",
                    "execloc_data" : [
                      {
                        "ext" : ".tex",
                        "patterns" : ["A_*.tex"] ,
                        "command": ["latexmk", "-f", "-pdf"]
                      },
                      {
                        "ext" : ".asy",
                        "patterns" : ["E*_*.asy","C*_*.asy"] ,
                        "command": ["asy","-f","pdf"]
                      },
                      {
                        "ext" : ".py",
                        "patterns" : ["*_fig.py"] ,
                        "command": ["python3"]
                      }
                    ],
                    "publish_data" : {
                      "patterns": ["A_*.pdf"],
                      "liste" : ["A_"]
                    },
                    "espace" : {
                      "region_name" : "fra1",
                      "endpoint_url" : "https://fra1.digitaloceanspaces.com",
                      "bucket" : "maquisdoc-math",
                      "prefix" : "math-exos/"
                    },
                    "bdg" : {}
                  }
.

        Returns
        -------
        None.

        """
        lineprefix = "\n \t \t"
        self.log = lineprefix + "Initialisation de la classe Execlocal."

        self.execloc_data = depot_data['depot']['execloc_data']
        self.rel_path = depot_data['depot']['relative_path']
        self.publish_data = depot_data['depot']['publish_data']

        # change de répertoire
        maintenance_path = os.getcwd()
        os.chdir(self.rel_path)

        # importation du module spécifique
        # exécution de la maintenance des fichiers LateX
        module = depot_data['depot']['execloc_module']
        if module:
            try:
                specific = importlib.import_module(module)
                self.log += lineprefix
                self.log += "Importation du module spécifique " + module
                self.log += specific.exec()
            except ImportError as error:
                self.log += lineprefix + "Module " + error.name + " pas trouvé"

        # liste des commandes de compilation à exécuter
        self.cmds_list = self.aexecuter()

        # compilations
        # print('\n')
        # for obj in self.cmds_list:
        #    print(obj, '\n')
        self.compil()

        self.publiables = self.apublierImg()
        # fichiers publiables dict path: date"""

        # retour au répertoire de base
        os.chdir(maintenance_path)

    def aexecuter(self):
        """
        Associe à chaque type de commande, la liste des fichiers à compiler par cette commande.

        Returns
        -------
        aexec : TYPE liste d'objets
            DESCRIPTION chaque objet code une série de commande.

        """
        self.log += ("\n \t \t Formation de la liste "
                     + "des commandes de compilation")
        aexec = []
        for type in self.execloc_data:
            obj = {'ext': type['ext'],
                   'imgdir': type['imgdir'],
                   'imgext': type['imgext'],
                   'command': type['command'],
                   'fics': []}
            imgext = type['imgext']
            imgdir = type['imgdir']
            fics = []
            # print(obj['command'], type['patterns'])
            for paty in type['patterns']:
                paty = self.rel_path + paty
                fics.extend(glob.glob(paty))

            for src in fics:
                srcext = os.path.splitext(src)[1]
                didi = os.path.dirname(src)
                img = os.path.join(didi, imgdir, os.path.basename(src))
                img = img.replace(srcext, imgext)
                # if ("A_" in src):
                #    print(src, img)
                if scantex.acompiler(src, img):
                    obj['fics'].append(src)
            aexec.append(obj)
        return aexec

    def apublierImg(self):
        """
        Renvoie un dictionnaire
            clé = chemin d'un fichier à publier
            valeur = timestamp du fichier
        """
        self.log += "\n \t \t Récup timesstamps"
        self.log += " locaux des fichiers à publier \n"
        docs_n = []
        times = {}
        for paty in self.publish_data['patterns']:
            docs_n += glob.glob(paty)
        for nom_doc in docs_n:
            times[self.rel_path + nom_doc] = os.path.getmtime(nom_doc)
        return times

    def compil(self):
        """
        Exécution des commandes de compilation.
        """
        self.log += '\n \t \t Exécution des compilations \n'
        log = ''
        for obj in self.cmds_list:
            log += '\t \t \t'
            log += (str(len(obj['fics'])) + ' commandes '
                    + str(obj['command']) + ' fichiers : \n')
            for src in obj['fics']:
                log += '\t \t \t \t' + src
                command = obj['command'] + [src]
                try:
                    # print(command)
                    subprocess.run(command)
                    log += ' OK \n'
                except subprocess.SubprocessError:
                    log += ' ERREUR dans exécution de la commande \n'
        self.log += log
