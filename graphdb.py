# -*- coding: utf-8 -*-
"""
Module d'interface avec la base de données en graphe.

Modifié le 24/01/23   @author: remy
"""
import neo4j

def format_cypher( param):
    """
    Renvoie une requête cypher.
    
    Dans la chaîne modèle
    
        "MATCH (n: {label} {propsF}) RETURN {propsR}"
        
    remplace les variables entre accolades par les valeurs dans `param`.
    Utilise la méthode `.format()` d'une chaine.

    #### Parametres
    
    param : TYPE dictionnaire
        DESCRIPTION exemple:
            
            {'label' : "Document", 
             'propsF' :"{typeDoc:'problème'}", 
             'propsR' : "n.titre, n.description"}.

    #### Returns
    
    req : TYPE chaine de caractères
        DESCRIPTION requête cypher.

    """
    req = "MATCH (n: {label} {propsF}) RETURN {propsR}"
    req = req.format(**param)
    return req
    

class Maquis:
    """
    Classe Maquis. Interface la base de données neo4j
    """
    def __init__(self,connect_data, loc_indexations, loc_descriptions):
        """
        
        #### Paramètres
        
        #### Renvoie
        
        None.

        """
        self.log = "\t Initialisation de la classe Maquis \n"
        URI = connect_data['URI']
        AUTH = (connect_data['user'], connect_data['password'])
    
                
        def do_cypher_tx(tx, cypher):
            result = tx.run(cypher)
            values = [record.values() for record in result]
            return values
        
        # descriptions
        #label = "Document"
        #propsF ="{typeDoc:'problème'}"
        #propsR = "n.titre, n.description"
        
        #req = "MATCH (n: {label} {propsF}) RETURN {propsR}"
        #req = req.format(label = label,
        #                 propsF = propsF,
        #                 propsR = propsR)
        param = {'label' : "Document", 
                 'propsF' :"{typeDoc:'problème'}", 
                 'propsR' : "n.titre, n.description"}
        req = format_cypher(param)

        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            rem_descriptions = session.execute_read(do_cypher_tx, req)
                
        print("coucou du module graphdb")
        
        loc_descriptions.sort(key=lambda descrpt : descrpt[0])
        rem_descriptions.sort(key=lambda descrpt : descrpt[0])
        print(loc_descriptions[0], rem_descriptions[0])
        print(len(loc_descriptions), len(rem_descriptions))
