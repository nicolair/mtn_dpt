# -*- coding: utf-8 -*-
"""
Exécute localement les scripts préliminaires à la publication et à la contextualisation des sources d'un dépôt.

Modifié le 03/03/23 @author: remy

Traitements à effectuer sur les fichiers d'un dépôt : 

- créer-modifier les sources avant compilation
- compiler
- établir des listes de fichiers images à publier
- établir des listes de données à contextualiser

Le module `execlocal`
- Importe le sous-module [`scantex`](scantex.html) d'examen des fichiers LateX.
- Définit la classe `Execlocal`.

Les traitements sont effectués lors de l'instanciation d'un objet `Execlocal`. Cette instanciation importe un module spécifique au dépôt.  
Actuellement, les sous-modules spécifiques sont 
[`exl_mathExos`](exl_mathExos.html) et 
[`exl_mathPbs`](exl_mathPbs.html).

Les commandes de compilation sont codées dans le fichier `init` (manifeste) du dépôt. Elles sont lancées par la méthode `compil()` de la classe `Execlocal`. Les autres traitements sont définis dans la fonction `exec()` du sous-module spécifique.

Principales propriétés d'un objet `Execlocal` :

- `.log`: journal de l'exécution locale
- `.publiables`: liste des fichiers publiables
- `.specific_results`: dictionnaire présentant des données spécifiques au dépôt.


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
        - exécute les traitements spécifiques
            - renseigne  `.specific_results`
        - exécute les commandes de compilation
            - renseigne `.publiables`
        

        #### Parametres

        data :

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

        self.commandes = data['commandes']
        self.rel_path = data['relative_path']
        self.publish_data = data['publish_data']
        self.context_data = data['context_data']

        # change de répertoire
        maintenance_path = os.getcwd()
        os.chdir(self.rel_path)

        # importation du module spécifique
        module = data['modulespec']
        if module:
            try:
                specific = importlib.import_module(module)
                self.log += lineprefix
                self.log += "Importation du module spécifique " + module
                # maintenance spécifique
                truc = specific.exec(data)
                self.log += truc['log'] 
                self.specific_results = truc['specific_results']
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
