# -*- coding: utf-8 -*-
"""
Interface avec le dossier local du dépôt. Exécute localement les scripts de
 maintenance des sources d'un dépôt.

Modifié le 14/02/23 @author: remy

- Importe le sous-module [`scantex`](scantex.html) d'examen des fichiers LateX.
- Définit la classe `Execlocal`.

L'instanciation d'un objet `Execlocal` traite les fichiers sources.

Le traitement des fichiers sources (LateX, ...) consiste en :

  - création-modification des sources avec un sous-module *spécifique*
  - compilation des sources vers les fichiers publiables.
  - examen des fichiers .idx d'index constitués lors de la compilation

Un objet `Execlocal`  présente

- la liste des fichiers publiables dans la propriété `.publiables`.
- la liste des indexations dans la propriété `.indexations`.

Sous-modules spécifiques pour les dépôts actuels:
[`exl_mathExos`](exl_mathExos.html)
[`exl_mathPbs`](exl_mathPbs.html)

"""
import importlib
import subprocess
import glob
import os.path

import scantex


class Execlocal:
    """Classe d'exécution locale."""

    def __init__(self, data):
        """
        Instancie un objet `Execlocal`.

        - récupère les paramètres du dépôt
        - initialise la propriété journal (`.log`)
        - importe le module spécifique au dépôt
        - exécute
            - scripts python spécifiques maj fichiers LateX
            - commandes de compilation
        - renseigne la propriété `.publiables`
        - renseigne la propriété `.indexations`

        #### Parametres

        depot_data :

        - TYPE dictionnaire
        - DESCRIPTION   codage du *manifeste* du dépôt

        La structure de ce dictionnaire est précisée dans le fichier
        d'initialisation spécifique [`init_mathExos`](init_mathExos.html)
        [`init_mathPbs`](init_mathPbs.html)

        #### Renvoie

        None.


        """
        lineprefix = "\n \t \t"
        self.log = lineprefix + "Initialisation de la classe Execlocal."
        """
        Journal d'instanciation d'un objet `Execlocal`.

        TYPE chaine de caractères.
        """

        # self.execloc_data = depot_data['depot']['execloc_data']
        self.commandes = data['commandes']
        # self.rel_path = depot_data['depot']['relative_path']
        self.rel_path = data['relative_path']
        #self.publish_data = depot_data['depot']['publish_data']
        self.publish_data = data['publish_data']
        #self.context_data = depot_data['depot']['context_data']
        self.context_data = data['context_data']

        # change de répertoire
        maintenance_path = os.getcwd()
        os.chdir(self.rel_path)

        # importation du module spécifique
        # module = depot_data['depot']['execloc_module']
        module = data['modulespec']
        if module:
            try:
                specific = importlib.import_module(module)
                self.log += lineprefix
                self.log += "Importation du module spécifique " + module
                # maintenance des fichiers LateX
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

        # renseigne la propriété .publiables
        self.publiables = self.apublierImg()
        # fichiers publiables dict path: date

        # renseigne la propriété .indexations
        idx_path_pattern = self.context_data['idx_path_pattern']
        self.indexations = scantex.get_liste_indexations(idx_path_pattern)
        self.log += lineprefix + str(len(self.indexations)) + " indexations \n"

        # renseigne la propriété .description
        description_pattern = self.context_data['description']
        self.descriptions = scantex.get_liste_descriptions(description_pattern)
        self.log += lineprefix + str(len(self.descriptions)) + " descriptions \n"

        # retour au répertoire de base
        os.chdir(maintenance_path)

    def aexecuter(self):
        """
        Renvoie une liste d'objets codant des commandes de compilation.

        Associe à chaque type de commande la liste des fichiers sur lesquels
        elle doit s'appliquer.

        Structure de l'objet codant un type de commande:

            obj = {'ext': type['ext'],
                   'imgdir': type['imgdir'],
                   'imgext': type['imgext'],
                   'command': type['command'],
                   'fics': []}


        """
        self.log += ("\n \t \t Formation de la liste "
                     + "des commandes de compilation")
        aexec = []
        for type in self.commandes:
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
                # print(paty, os.getcwd())
                fics.extend(glob.glob(paty))
                # print(fics,"\n")

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
        Renvoie un dictionnaire de fichiers publiables.

        - clé = chemin d'un fichier à publier
        - valeur = timestamp du fichier
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
        Exécute les commandes de compilation.

        Elles sont codées dans `self.cmds_list`.
        Un compte rendu est placé dans le journal `self.log`.
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
