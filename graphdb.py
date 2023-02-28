# -*- coding: utf-8 -*-
"""
Interface avec la partie de la base de données en graphe reflétant le dépôt.
Modifié le 15/02/23   @author: remy

- Définit des outils utiles pour tous les dépôts
- Importe le sous-module `bdg_xxxx` spécifique au dépôt sous le nom `specific`.
- Définit la classe `Maquis`.

La maintenance de la base est réalisée par des requêtes cypher définies
 dans `specific` et exécutés lors de l'instanciation de la classe `Maquis`
 par l'appel `specific.exec()`.

"""
import importlib
# import neo4j


class Maquis:
    """
    Classe Maquis. Interface la base de données neo4j.

    connect_data est obsolète.
    """

    def __init__(self, data, loc_indexations, loc_descriptions):
        """
        Instanciate.

        #### Paramètres

        #### Renvoie

        None.

        """
        self.log = "\t Initialisation de la classe Maquis \n"
        self.loc_indexations = loc_indexations
        self.loc_descriptions = loc_descriptions

        print("coucou du module graphdb")

        lineprefix = "\n \t \t"

        # Importation du module spécifique
        module = data['modulespec']
        if module:
            try:
                specific = importlib.import_module(module)
                self.log += lineprefix
                self.log += "Importation du module spécifique " + module
                # execécution des scripts de contextualisation
                self.log += specific.exec(self, data)
            except ImportError as error:
                self.log += lineprefix + "Module " + error.name + " pas trouvé"


    def format_cypher_RETURN(self, param):
        """
        Renvoie une requête cypher de type `RETURN`.

        Dans la chaîne modèle

            "MATCH (n: {label} {propsF}) RETURN {propsR}"

        remplace les variables entre accolades par les valeurs dans `param`.
        Utilise la méthode `.format()` d'une chaine.

        #### Parametres

        param : TYPE dictionnaire
            DESCRIPTION exemple:

            {'label': "Document",
             'propsF':" {typeDoc:'problème'}",
             'propsR': "n.titre, n.description"}.

        #### Renvoie

        TYPE chaine de caractères
        DESCRIPTION requête cypher.

        """
        req = "MATCH (n: {label} {propsF}) RETURN {propsR}"
        req = req.format(**param)
        return req

    def format_cypher_DELETE(self, param):
        """
        Renvoie une requête cypher de type `DETACH DELETE`.

        ATTENTION ! Ce type de requte est à manier avec précaution.
         Toujours vérifier ce qui sera détruit.

        Dans la chaîne modèle

            "MATCH (n: {label} {propsF}) DETACH DELETE n"

        remplace les variables entre accolades par les valeurs dans `param`.
        Utilise la méthode `.format()` d'une chaine.

        #### Parametres

        param : TYPE dictionnaire
           DESCRIPTION exemple pour supprimer le problème de titre 'grpe2'
           dans la base:

            {'label' : "Document",
             'propsF' :"{typeDoc:'problème' titre:'grpe2'}"}

        #### Renvoie

        TYPE chaine de caractères
        DESCRIPTION requête cypher.

        """
        req = "MATCH (n: {label} {propsF}) DETACH DELETE n"
        req = req.format(**param)
        return req

    def format_cypher_SET(self, param):
        """
        Renvoie une requête cypher de type `SET`.

        Dans la chaîne modèle

            "MATCH (n: {label} {propsF}) SET {propsV}"

        remplace les variables entre accolades par les valeurs dans `param`.
        Utilise la méthode `.format()` d'une chaine.

        #### Parametres

        param : TYPE dictionnaire
            DESCRIPTION exemple:

            {'label' : "Document",
             'propsF' :"{typeDoc:'problème'}",
             'propsV' : "n.description = tagada"}.

        #### Renvoie

        TYPE chaine de caractères
        DESCRIPTION requête cypher.

        """
        req = "MATCH (n: {label} {propsF}) SET {propsV}"
        req = req.format(**param)
        return req

    def do_cypher_tx(self, tx, cypher):
        """
        Exécute une requête cypher et renvoie les valeurs retournées.

        #### Parametres

        tx: TYPE transaction neo4j DESCRIPTION lié à la session neo4j
        *pas clair!*

        cypher: TYPE chaine de caractères DESCRIPTION requête cypher

        #### Renvoie

        TYPE liste

        DESCRIPTION valeurs retournées par la requête
        """
        result = tx.run(cypher)
        values = [record.values() for record in result]
        return values
