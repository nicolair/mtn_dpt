#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La contextualisation du dépôt de problèmes consiste à s'assurer que la base en graphe reflète les problèmes et leurs méta-données locales. Ces méta-données sont définies par l'auteur c'est à dire écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Modifié le 05/03/23 @author: remy

La fonction `exec()` est appelée lors de l'instanciation de la classe `Maquis`. Elle maintient cette cohérence en exécutant des requêtes cypher.

Quelles sont les méta-données définies par l'auteur d'un problème?
- une description
- des index

Un utilisateur autre que l'auteur doit pouvoir aussi associer des méta-données à un problème. La base en graphe reflète une méta-donnée de manière différente selon qu'elle est définie par l'auteur ou par un utilisateur. 

La définition de méta-données par un utilisateur n'est pas encore implémentée.

#### Noeud et description associés à un problème.

L'auteur définit une description d'un problème en l'insérant entre des tags dans le fichier Latex de l'énoncé. Exemple avec le début de `Eprob4.tex`

    %<dscrpt>Lancers de pièces.</dscrpt>
    On dispose de deux pièces de monnaie discernables, désignées dans la suite
    de l'exercice par \og pièce 1\fg~ et \og pièce 2\fg. On ...

Un noeud labélisé `Document` est associé au problème `prob4`. La description définie dans le code source est la propriété `description` du noeud.

Les lignes suivantes présentent la requête cypher pour extraire ce noeud 

    MATCH (d:Document {typeDoc:"problème", titre:"prob4"}) RETURN d
    
et le noeud renvoyé

    {
    "identity": 7214,
    "labels": [
        "Document"
    ],
    "properties": {
        "date": "2018-05-06T21:36:11Z",
        "titre": "prob4",
        "urlSrcEnon": "https://github.com/nicolair/math-pbs/blob/master/Eprob4.tex",
        "typeDoc": "problème",
        "urlSrcCorr": "https://github.com/nicolair/math-pbs/blob/master/Cprob4.tex",
        "description": "Lancers de pièces.",
        "url": "https://maquisdoc-math.fra1.digitaloceanspaces.com/maths-pbs/Aprob4.pdf"
    },
    "elementId": "7214"
    }
    
Une description insérée par un autre utisateur serait contenue dans la propriété `texte` d'un noeud labélisé `Commentaire` et relié au document `prob4` par une arête labélisée `DÉCRIT`. Ceci n'est pas encore implémenté.

#### Index associés à un problème.

Les index sont définis dans la source LateX par la commande `\index`. Lors de la compilation, un fichier `.idx` est créé qui permet localement d'associer l'index et le problème. Du côté de la base en graphe, un index est un noeud labelisé `Concept`. Une arête labélisée `INDEXE` issue du noeud associé au problème pointe vers le noeud associé à l'index.

Si on considère l'arête dans l'autre sens c'est à dire pointant de l'index vers le problème, un index apparait comme un mot-clé.  
Un mot-clé défini par un utilisateur sera défini avec une arète dont la source est le noeud représentant le mot et dont la cible est le noeud représentant le problème. Cette fonctionnalité n'est pas encore implémentée et les labels du noeud représentant le mot et de l'arête ne sont pas fixés. 

"""
import neo4j

def exec(self):
    """
    Exécution des requêtes spécifques de maintenance de la base.
    - récupération des descriptions dans la base 
    - supprimer dans la base les problèmes absents localement
    - créer dans la base les problèmes locaux manquants
    - si description locale et distante différentes,
        - copier description locale sur distante
    - afficher les indexations locales

    #### Renvoie

    log: str journal

    """
    print("coucou de exec() dans bdg_mathPbs.py")
    
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)
    
    loc_indexations = self.specific_results['indexations']
    loc_descriptions = self.specific_results['descriptions']

    param = {'label' : "Document", 
             'propsF' :"{typeDoc:'problème'}", 
             'propsR' : "n.titre, n.description"}
    req = self.format_cypher_RETURN(param)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_descriptions = session.execute_read(self.do_cypher_tx, req)

    loc_descriptions.sort(key=lambda descrpt: descrpt[0])
    rem_descriptions.sort(key=lambda descrpt: descrpt[0])
    
    # Nbs de problèmes
    blabla = "Nbs de pbs. local: {nloc},  base: {nrem}"
    blabla = blabla.format(
        nloc=len(loc_descriptions),
        nrem=len(rem_descriptions))
    print(blabla)

    # Noeuds isolés (orphelins)
    nomsR = [descrpR[0] for descrpR in rem_descriptions]
    nomsL = [descrpL[0] for descrpL in loc_descriptions]
    rem_orphs = []
    for nom in nomsR:
        if nom not in nomsL:
            rem_orphs.append(nom)
    blabla = "\n Pbs distants sans source locale (à supprimer) : {}"
    blabla = blabla.format(rem_orphs)
    print(blabla)
    for nom in rem_orphs:
        param = {'label' : "Document"}
        param['propsF'] = 'typeDoc:"problème", titre:"{titre}"'
        param['propsF'] = param['propsF'].format(titre=nom)
        param['propsF'] = '{' + param['propsF'] + '}'
        req = self.format_cypher_DELETE(param)
        print(req)
        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)
        print(val)

    # Problèmes sans noeud associé
    loc_orphs = []
    for nom in nomsL:
        if nom not in nomsR:
           loc_orphs.append(nom)
    blabla = "\n Pbs locaux sans reflet distant (à écrire) : "
    blabla = blabla.format(loc_orphs)
    print(blabla)

    # Descriptions
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
            'nomL': nomL,
            'descrpL': descrpL,
            'nomR': nomR,
            'descrpR': descrpR
        }

        if nomL == nomR and descrpL != descrpR:
            print(blabla.format(**params))
            param['label'] = 'Document'
            param['propsF'] = 'typeDoc:"problème", titre:"{titre}"'
            param['propsF'] = param['propsF'].format(titre=nomR)
            param['propsF'] = '{' + param['propsF'] + '}'
            param["propsV"] = 'n.description = "{descrpL}"'
            param["propsV"] = param["propsV"].format(descrpL=descrpL)
            req = self.format_cypher_SET(param)
            print(req)
            with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
                val = session.execute_write(self.do_cypher_tx, req)
                print(val)

    # indexations
    #print("\n Indexations locales")
    indexe(self,loc_indexations)


    log = ""
    return log

def indexe(self, loc_indexations):
    '''
        Assure que des relations `INDEXE` sont associées aux indexations locales.
    '''
    print("\n coucou de indexe()")
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)

    # indexations dans le graphe
    req = ''' MATCH (p:Document {typeDoc:"problème"}) -[:INDEXE]-> (c:Concept)
    RETURN "A" + p.titre, c.litteral
    '''
    #print(req)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_indexations = session.execute_write(self.do_cypher_tx, req)

    print(rem_indexations)
    print(loc_indexations)

        # création des indexations manquantes dans le graphe
    req = ''' MATCH (p:Document {{typeDoc:"problème", titre: "{0}"}})
    MERGE (c:Concept {{litteral:"{1}"}})
    CREATE (p)-[:INDEXE]->(c)
    '''
    rem_index_orph = []
    for index in loc_indexations :
        if index not in rem_indexations:
            nom = index[0][1:]
            concept = index[1]
            req1 = req.format(nom, concept)
            print(nom, concept, req1)
            with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
                val = session.execute_write(self.do_cypher_tx, req1)

