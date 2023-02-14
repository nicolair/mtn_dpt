# -*- coding: utf-8 -*-
"""
Module d'interface avec la base de données en graphe.

Modifié le 24/01/23   @author: remy
"""
import neo4j

def format_cypher_RETURN( param):
    """
    Renvoie une requête cypher de type `RETURN`.
    
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

    #### Renvoie
    
    TYPE chaine de caractères
    DESCRIPTION requête cypher.

    """
    req = "MATCH (n: {label} {propsF}) RETURN {propsR}"
    req = req.format(**param)
    return req
    
def format_cypher_DELETE( param):
    """
    Renvoie une requête cypher de type `DETACH DELETE`.

    ATTENTION ! Ce type de requte est à manier avec précaution. Toujours vérifier ce qui sera détruit.

    Dans la chaîne modèle

        "MATCH (n: {label} {propsF}) DETACH DELETE n"

    remplace les variables entre accolades par les valeurs dans `param`.
    Utilise la méthode `.format()` d'une chaine.

    #### Parametres

    param : TYPE dictionnaire
        DESCRIPTION exemple pour supprimer le problème de titre 'grpe2' dans la base:

            {'label' : "Document",
             'propsF' :"{typeDoc:'problème' titre:'grpe2'}"}

    #### Renvoie

    TYPE chaine de caractères
    DESCRIPTION requête cypher.

    """
    req = "MATCH (n: {label} {propsF}) DETACH DELETE n"
    req = req.format(**param)
    return req

def format_cypher_SET( param):
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


def do_cypher_tx(tx, cypher):
    """
    Exécute une requête cypher et renvoie les valeurs retournées.

    #### Parametres

    tx: TYPE transaction neo4j DESCRIPTION lié à la session neo4j *pas clair!*

    cypher: TYPE chaine de caractères DESCRIPTION requête cypher

    #### Renvoie

    TYPE liste

    DESCRIPTION valeurs retournées par la requête
    """
    result = tx.run(cypher)
    values = [record.values() for record in result]
    return values

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
    
        param = {'label' : "Document", 
                 'propsF' :"{typeDoc:'problème'}", 
                 'propsR' : "n.titre, n.description"}
        req = format_cypher_RETURN(param)

        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            rem_descriptions = session.execute_read(do_cypher_tx, req)
                
        print("coucou du module graphdb")
        
        loc_descriptions.sort(key=lambda descrpt : descrpt[0])
        rem_descriptions.sort(key=lambda descrpt : descrpt[0])

        # Nbs de problèmes
        blabla = "Nbs de pbs. local: {nloc},  base: {nrem}".format(nloc=len(loc_descriptions),
                                                                   nrem=len(rem_descriptions)) 
        print(blabla)

        #Noeuds isolés (orphelins)
        nomsR = [descrpR[0] for descrpR in rem_descriptions]
        nomsL = [descrpL[0] for descrpL in loc_descriptions]
        rem_orphs = []
        for nom in nomsR:
            if nom not in nomsL:
                rem_orphs.append(nom)
        blabla = "Pbs ds neo4j sans source locale (à supprimer) : {}".format(rem_orphs) 
        print(blabla)

        loc_orphs = []
        for nom in nomsL:
            if nom not in nomsR:
                loc_orphs.append(nom)
        blabla = "Pbs locaux sans reflet dans neo4j (à écrire) : ".format(loc_orphs)
        print(blabla)

        #Descriptions 
        print("\n Descriptions différentes local/base, requête cypher")
        n = min(len(loc_descriptions), len(rem_descriptions))
        blabla = "-------\n"
        blabla += "LOCAL nom: {nomL} description: {descrpL} \n"
        blabla += "REMOTE nom: {nomR} description: {descrpR}\n"

        for i in range(n):
            nomL = loc_descriptions[i][0]
            descrpL = loc_descriptions[i][1]
            nomR = rem_descriptions[i][0]
            descrpR = rem_descriptions[i][1]
            params = {
                'nomL' : nomL,
                'descrpL' : descrpL,
                'nomR' : nomR,
                'descrpR' : descrpR
            }

            if nomL == nomR and descrpL != descrpR:
                print(blabla.format(**params))
                param['label'] = 'Document'
                param['propsF'] = 'typeDoc:"problème", titre:"{titre}"'.format(titre=nomR)
                param['propsF'] = '{' + param['propsF'] + '}'
                param["propsV"] = 'n.description = "{descrpL}"'.format(descrpL=descrpL)
                req = format_cypher_SET(param)
                print(req)

        #index
        print("\n Indexations locales")
        print(loc_indexations)
