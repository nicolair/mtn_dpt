"""
Module principal de maintenance d'un dépôt.

Modifié le 09/01/23  @author: nicolair

- Importe les modules
    - [`execlocal`](execlocal.html)
    - [`espace`](espace.html)
    - à définir (contextualisation).

- Définit la classe `Depot`.

Le module `execlocal` définit la classe `Execlocal`. L'instanciation de cette
classe réalise

   - la maintenance des fichiers Latex
   - les compilations des images
   - place la liste des images publiables dans une propriété.

Le module `espace` définit la classe `Espace`. L'instanciation de cette
classe met à jour l'espace de publication selon l'état des images publiables
 dans le dépôt local.

La propriété `.log` contient le journal des instanciations.

"""
import os
import sys
import execlocal
import espace
import graphdb

# pour permettre l'import programmatique
localpath = os.path.dirname(__file__)
if localpath not in sys.path:
    sys.path.append(os.path.dirname(__file__))


class Depot():
    """
    Classe représentant un dépôt.

    La maintenance du dépôt est réalisée lors de l'instanciation.

    """

    def __init__(self, data):
        """
        Instancie un objet `Depot`.

        - Définit une propriété `.log` : journal de la maintenance.
        - Instancie une classe d'exécution locale `Execlocal`
            - maintenance des fichiers Latex
            - compilations diverses
        - Ajoute le `.log` de l'instance de `Execlocal` au `.log` du `Depot`.
        - Instancie une classe de publication `Espace`
            - maintenance de l'espace dédié au dépôt.
        - Ajoute le `.log` de l'instance d' `Espace` au `.log` du `Depot`.
        - Instancie une classe de contextualisation `Maquis`.
        - Ajoute le `.log` de l'instance de `Maquis` au `.log` du `Depot`.

        #### Parametres

        - data :
            - TYPE dictionnaire
            - DESCRIPTION code le manifeste du dépôt

        La structure de ce dictionnaire est précisée dans le fichier
        d'initialisation spécifique [`init_mathExos`](init_mathExos.html)
        [`init_mathPbs`](init_mathPbs.html)

        #### Renvoie

        None.

        """
        self.log = "\n \t Initialisation de la classe Depot : "
        """
        Journal d'instanciation d'un objet `Depot`.

        TYPE chaine de caractères.
        """

        self.nom = data['nom']
        # self.nom = depot_data['depot']['nom']

        #self.rel_path = depot_data['depot']['relative_path']
        self.rel_path = data['execloc']['relative_path']
        #self.execloc_data = depot_data['depot']['execloc_data']
        #self.execloc_module = depot_data['depot']['execloc_module']
        self.execloc_module = data['execloc']['modulespec']

        # classe d'exécution locale
        exl = execlocal.Execlocal(data['execloc'])
        self.publiables = exl.publiables
        self.log += exl.log

        # classe de publication
        # for fic in self.publiables.keys():
        #    print(fic)
        esp = espace.Espace(data['espace'], self.publiables)
        self.log += esp.log

        # classe de contextualisation
        maquisdoc = graphdb.Maquis(data['context'],
                                   exl.indexations,
                                   exl.descriptions)
        self.log += maquisdoc.log
