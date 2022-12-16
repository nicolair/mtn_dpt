# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 08:11:02 2017

@author: nicolair

Module principal de maintenance d'un dépot.
Importe les modules execlocal et espace.
Instancie des classes Execlocal et Espace.

L'instanciation de la classe Execlocal exécute
    - la maintenance des fichiers Latex
    - les compilations des images
    - place la liste des images publiables dans une propriété.

L'instanciation de la classe Espace exécute la maintenance de l'espace dédié.

La propriété `.log` contient le journal des instanciations.

"""
import os
import sys
import execlocal
import espace

# pour permettre l'import programmatique
localpath = os.path.dirname(__file__)
if localpath not in sys.path:
    sys.path.append(os.path.dirname(__file__))


class Depot():
    """
    Classe représentant un dépot.

    La maintenance est réalisée lors de l'instanciation.

    """

    def __init__(self, depot_data):
        """
        Initialise.

        Définit une propriété `log` : journal de la maintenance
        Instancie une classe d'exécution locale
            maintenance des fichiers Latex
            compilations diverses
        Instancie une classe de publication
            maintenance de l'espace dédié au dépôt.
        Instancie une classe de contextualisation

        Parameters
        ----------
        depot_data : TYPE dictionnaire
            DESCRIPTION code le manifeste du dépôt
            exemple pour mathExos
            ---------------------              {
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
              }.

        Returns
        -------
        None.

        """
        self.log = "\n \t Initialisation de la classe Depot : "

        self.nom = depot_data['depot']['nom']
        self.rel_path = depot_data['depot']['relative_path']
        self.execloc_data = depot_data['depot']['execloc_data']
        self.execloc_module = depot_data['depot']['execloc_module']

        # classe d'exécution locale
        exl = execlocal.Execlocal(depot_data)
        self.publiables = exl.publiables
        self.log += exl.log

        # classe de publication
        # for fic in self.publiables.keys():
        #    if 'A_' in fic:
        #        print(fic)
        esp = espace.Espace(depot_data['espace'], self.publiables)
        self.log += esp.log

        # classe de contextualisation

    def acontextualiser(self):
        """Renvoie les données à mettre à jour dans le graphe neo4j."""
        noeuds = []
        relations = []
        for obj in self.context_data:
            truc = obj['extraire'](obj['para'])
            noeuds.extend(truc['noeuds'])
            relations.extend(truc['relations'])
        return {'noeuds': noeuds, 'relations': relations}
