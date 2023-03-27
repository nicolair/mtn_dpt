#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La contextualisation du dépôt d'exercices  s'assure que la base en graphe reflète les exercices et leurs méta-données locales. Ces méta-données sont définies par l'auteur c'est à dire écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Modifié le 26/03/23 @author: remy

La fonction `exec()` est appelée lors de l'instanciation de la classe `Maquis`. Elle met à jour la base en fonction de l'état du dépôt en exécutant des requêtes cypher.


#### Noeuds et arêtes
Les éléments du graphe associés aux exercices détaillés dans le [manifeste](init_mathExos.html).

- noeud exercice: label: `Document`,  `typeDoc: "exercice", discipline: "mathématique", titre: "cdxx"`
- noeud thème: label; `Concept`, `litteral: "nom du thème"`
- noeud feuille: label: `Document`, `typeDoc: "liste exercices", titre: "nom du thème"`
- arête (`CONTIENT`) entre une feuille et un exercice
- arête (`EVALUE`) entre un exercice et le concept de son thème
- arête (`EVALUE`) entre une feuille et le concept de son thème
- arête (`INDEXE`) entre un exercice et un concept indexé

"""
import neo4j
import locale
import functools
locale.setlocale(locale.LC_ALL, '')

def exec(self):
    """
    Exécution des requêtes spécifques de maintenance de la base.
    - les données locales (feuilles et exercices) ont été formées par l'exécution locale spécifique et sont passées par le paramètre `specific_results`.
    - récupération dans la base des patterns

        (feuille) -[:CONTIENT]-> (exercice) -[:EVALUE]-> (concept)
    - affichage des feuilles par ordre alphabétique des thèmes
    - comparaison des exercices locaux et dans le graphe (orphelins)
    - création des patterns pour les exercices locaux absents du graphe
    - création des patterns pour les indexations locales absentes du graphe.

    #### Renvoie

    log: str journal

    """
    print("coucou de exec() dans bdg_mathExos.py")
    
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)

    # données locales (dictionnaires)
    loc_dictExos = self.specific_results['listeExos']
    loc_exercices = []
    for code,liste in loc_dictExos.items():
        loc_exercices += liste
    loc_exercices = list(map(
        lambda chaine: chaine.removeprefix('E').removesuffix('.tex'),
        loc_exercices))

    loc_themes = self.specific_results['themes']
    loc_indexations = self.specific_results['indexations']

    # Noeuds exercices du graphe
    param = {'label' : "Document",
             'propsF' :"{typeDoc:'exercice', discipline:'mathématique'}",
             'propsR' : "n.titre"}
    req = self.format_cypher_RETURN(param)
    # Nouvelle requête:
    new_req = 'MATCH (f:Document {typeDoc:"liste exercices"})-[:CONTIENT]-> (e:Document {typeDoc:"exercice", discipline:"mathématique"})-[:EVALUE]->(c:Concept) WHERE f.titre = c.litteral RETURN f.titre, e.titre, c.litteral ORDER BY e.titre'
    #print(new_req)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_feu_exo_con = session.execute_read(self.do_cypher_tx, new_req)
    #print(rem_feu_exo_con[0:3])
    rem_exercices = list(map(lambda x: x[1], rem_feu_exo_con))
    # print(rem_exercices[0:5])

    # codes et thèmes dans le graphe
    # codes des thèmes
    req = 'MATCH (f:Document {typeDoc:"liste exercices"})-[:CONTIENT]-> (e:Document {typeDoc:"exercice", discipline:"mathématique"}) RETURN DISTINCT f.titre, left(e.titre,2) AS code ORDER BY code'
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_theme_code = session.execute_read(self.do_cypher_tx, req)
    #print(rem_theme_code[0:5])
    themes = {l[1]:l[0] for l in rem_theme_code}

    # Noeuds feuilles d'exercices du graphe
    param = {'label' : "Document",
             'propsF' :"{typeDoc:'liste exercices'}",
             'propsR' : "n.titre"}
    req = self.format_cypher_RETURN(param)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_feuilles = session.execute_read(self.do_cypher_tx, req)
    rem_feuilles = list(map(lambda x: x[0], rem_feuilles))
    # pour bien ranger les accents
    rem_feuilles.sort(key=functools.cmp_to_key(locale.strcoll))
    i = 1
    print("\n thèmes des feuilles")
    for theme in rem_feuilles:
        print(i,theme)
        i += 1

    #Nbs d'exercices
    #print(loc_exercices)
    blabla = "\n Nbs d'exercices. local {nloc}, base {nrem}"
    blabla = blabla.format(
        nloc=len(loc_exercices),
        nrem=len(rem_exercices))
    print(blabla)

    # Noeuds exercices isolés (orphelins)
    rem_exos_orph = []
    for nom in rem_exercices:
        if nom not in loc_exercices:
            rem_exos_orph.append(nom)
    blabla = "\n Noeuds exercices distants sans source locale (à supprimer): {}"
    blabla = blabla.format(rem_exos_orph)
    print(blabla)
    for nom in rem_exos_orph:
        param = {'label' : "Document"}
        param['propsF'] = 'typeDoc:"exercice", discipline:"mathématique", titre:"{titre}"'
        param['propsF'] = param['propsF'].format(titre=nom)
        param['propsF'] = '{' + param['propsF'] + '}'
        req = self.format_cypher_DELETE(param)
        print(req)
        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)
        print(val)


    # Exercices locaux sans noeud associé
    loc_exos_orph = []
    for nom in loc_exercices:
        if nom not in rem_exercices:
            loc_exos_orph.append(nom)
    blabla = "\n Exercices locaux sans noeud associé (à créer): {}"
    blabla = blabla.format(loc_exos_orph)
    print(blabla)

    nouveaux_exos(self,loc_exos_orph, themes)

    # indexations
    #print("\n Indexations locales")
    indexe(self, loc_indexations)
    
    log = ""
    return log

def nouveaux_exos(self,loc_exos_orph,themes):
    """
    insertion dans le maquis des éléments associés à un exercice local sans noeud associé.

    Pour chaque exercice local absent du graphe
    - crée le noeud exercice
    - crée la relation feuille `CONTIENT` exercice
    - crée la relation exercice `EVALUE` concept

    Noter que le titre de la feuille contenant l'exercice est le littéral du concept évalué.

    On peut créer un nouvel exercice dans une feuille existante mais pas créer une nouvelle feuille.
    """
    print("\n coucou de nouvel_exo()")
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)

    for nom in loc_exos_orph:
        code = nom[:2]
        theme = themes[code]
        print(nom, code, theme)

        # créer le noeud exercice
        label = "Document"
        propsF = '{'
        propsF += 'date: datetime({epochMillis: timestamp()}), '
        propsF += 'titre: "' + nom +'", '
        propsF += 'urlSrcEnon: "https://github.com/nicolair/math-exos/blob/master/' + nom + '.tex", '
        propsF += 'typeDoc: "exercice", '
        propsF += 'discipline: "mathématique", '
        propsF +=  'url: "https://maquisdoc-math.fra1.digitaloceanspaces.com/math-exos/Aexo_' + nom + '.html" }'
        param = {'label': label, 'propsF': propsF}
        req = self.format_cypher_CREATE(param)
        #print(req)
        with neo4j.GraphDatabase.driver(URI,auth=AUTH).session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)

        # créer la relation feuille [CONTIENT] exercice
        req = '''MATCH (e:Document {{typeDoc:"exercice", titre: "{0}"}})
        MATCH (f:Document {{typeDoc: "liste exercices", titre: "{1}"}})
        CREATE (f) -[r:CONTIENT]-> (e)'''
        req = req.format(nom, theme)
        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)

        # créer la relation exercice [EVALUE] theme (concept)
        req = '''MATCH (e:Document {{typeDoc:"exercice", titre: "{0}"}})
        MATCH (c:Concept {{typeConcept: "thème feuille exercices", litteral: "{1}"}})
        CREATE (e) -[:EVALUE]-> (c)'''
        req = req.format(nom, theme)
        with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)

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
    req = ''' MATCH (e:Document {typeDoc:"exercice", discipline: "mathématique"}) -[:INDEXE]-> (c:Concept)
    RETURN "Aexo_" + e.titre, c.litteral
    '''
    #print(req)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
            rem_indexations = session.execute_write(self.do_cypher_tx, req)

    print(rem_indexations)
    print(loc_indexations)

    # création des indexations manquantes dans le graphe
    req = ''' MATCH (e:Document {{typeDoc:"exercice", discipline: "mathématique", titre: "{0}"}})
    MERGE (c:Concept {{litteral:"{1}"}})
    CREATE (e)-[:INDEXE]->(c)
    '''
    rem_index_orph = []
    for index in loc_indexations :
        if index not in rem_indexations:
            nom = index[0][5:]
            concept = index[1]
            req1 = req.format(nom, concept)
            with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
                val = session.execute_write(self.do_cypher_tx, req1)

