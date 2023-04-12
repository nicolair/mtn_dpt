#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La contextualisation du dépôt de cours consiste à s'assurer que la base en graphe reflète les textes de cours et leurs méta-données locales. Ces méta-données sont définies par l'auteur c'est à dire écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Modifié le 30/03/23 @author: remy

La fonction `exec()` est appelée lors de l'instanciation de la classe `Maquis`. Elle maintient cette cohérence en exécutant des requêtes cypher.

Quelles sont les méta-données définies par l'auteur d'un problème?
- des index

#### Noeud associé à un texte de cours.

Un noeud labélisé `Document` est associé à un texte de cours `C` et caractérisé par sa propriété titre qui est égale au titre dans le fichier Latex et pas au nom du fichier.  
Exemple pour le fichier C1616.tex.
Les premières lignes du fichier sont:
    \input{courspdf.tex}
    
    \debutcours{TFCA - Primitives et équations différentielles linéaires}{0.3 \tiny{\today}}
    
    \section{Calculs de primitives.}
    Les démonstrations des résultats admis dans cette section sont proposés dans le chapitre \href{\baseurl C2190.pdf}{Intégrales et primitives}.
    
    \subsection{Définition et primitives usuelles.}
    \subsubsection{Résultats admis.}
    \begin{defi}
    Une primitive d'une fonction $f$ définie dans un intervalle $I$ à valeurs complexes est une fonction $F$ dérivable dans $I$ et dont la dérivée est $f$. 
    \end{defi}

Les lignes suivantes présentent la requête cypher pour extraire ce noeud 

    MATCH (c:Document {typeDoc:"cours", titre:"Primitives et équations différentielles linéaires"}) RETURN c
    
et le noeud renvoyé

    {
      "identity": 0,
      "labels": [
        "Document"
      ],
      "properties": {
        "date": "2013-10-03T06:00:57Z",
        "titre": "Primitives et équations différentielles linéaires",
        "typeDoc": "cours",
        "urlSrc": "https://github.com/nicolair/math-cours/blob/master/C1616.tex",
        "discipline": "mathématiques",
        "url": "https://maquisdoc-math.fra1.digitaloceanspaces.com/math-cours/C1616.pdf"
      },
      "elementId": "0"
    }
    
#### Index définis dans un texte de cours.

Les index sont définis dans la source LateX par la commande `\index`. Lors de la compilation, un fichier `.idx` est créé qui permet localement d'associer l'index et le texte de cours. Du côté de la base en graphe, un index est un noeud labelisé `Concept`. Une arête labélisée `INDEXE` issue du noeud associé au texte de cours pointe vers le noeud associé à l'index.

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
    print("coucou de exec() dans bdg_mathCours.py")
    
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)
    
    loc_indexations = self.specific_results['indexations']
    loc_titres = self.specific_results['titres']
    print("\n Titres des textes de cours locaux")
    print(loc_titres)
    
    # noeuds textes de cours
    param = {'label' : "Document", 
             'propsF' :'{typeDoc:"cours", discipline:"mathématique"}', 
             'propsR' : 'substring(n.urlSrc,51), n.titre'}
    req = self.format_cypher_RETURN(param)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_cours = session.execute_read(self.do_cypher_tx, req)
    print("\n Titres des noeuds textes de cours")
    rem_cours.sort(key=lambda paire: paire[0])
    print(rem_cours)
    
    # Nbs de textes de cours
    blabla = "\n Nbs de textes de cours. local: {nloc},  base: {nrem}"
    blabla = blabla.format(
        nloc= len(loc_titres), nrem=len(rem_cours))
    print(blabla)

    # indexations
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
    req = ''' MATCH (p:Document {typeDoc:"cours"}) -[:INDEXE]-> (c:Concept)
    RETURN "A" + p.titre, c.litteral
    '''
    #print(req)
    with neo4j.GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        rem_indexations = session.execute_write(self.do_cypher_tx, req)

    print("\n Indexations dans le graphe")
    print(rem_indexations)
    print("\n Indexations locales: {0}".format(len(loc_indexations)))
    print(loc_indexations)
"""
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

"""
