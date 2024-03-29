#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La contextualisation du dépôt de cours consiste à assurer que la base en graphe reflète les textes de cours et leurs méta-données locales. Pour cela, des noeuds Cours  sont associés aux fichiers Cours.

Les méta-données sont définies par l'auteur et écrites dans le dépôt local. La modification d'une méta-donnée de ce type se fait dans le dépôt et non dans la base en graphe.

Modifié le 10/12/23 @author: remy

La fonction `exec()` est appelée lors de l'instanciation de la classe `Maquis`. Elle appelle la fonction `indexe()`.

La fonction `indexe()`  maintient la cohérence en exécutant des requêtes cypher sur la base en graphe.

Quelles sont les méta-données définies par l'auteur d'un problème?
- des index

#### Noeud associé à un texte de cours.

Un noeud labélisé `Document` est associé à un texte de cours `C` et caractérisé par sa propriété titre qui est égale au titre dans le fichier Latex et pas au nom du fichier.  
Exemple pour le fichier C1616.tex.
Les premières lignes du fichier sont:

    \\input{courspdf.tex}
    
    \\debutcours{Primitives et équations différentielles linéaires}{0.3 \\tiny{\\today}}
    
    \\section{Calculs de primitives.}
    Les démonstrations des résultats admis dans cette section sont proposés dans le chapitre \\href{\\baseurl C2190.pdf}{Intégrales et primitives}.
    
    \\subsection{Définition et primitives usuelles.}
    \\subsubsection{Résultats admis.}
    \\begin{defi}
    Une primitive d'une fonction $f$ définie dans un intervalle $I$ à valeurs complexes est une fonction $F$ dérivable dans $I$ et dont la dérivée est $f$. 
    \\end{defi}

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

Les index sont définis dans la source LateX par la commande `\\index`. Lors de la compilation, un fichier `.idx` est créé qui permet localement d'associer l'index et le texte de cours. Attention, un index peut figurer plusieurs fois dans un document. La liste des indexations (paire fichier, litteral) calculée par `scantex` peut contenir plusieurs fois la même paire.

Du côté de la base en graphe, un index est un noeud labelisé `Concept`. Une arête labélisée `INDEXE` issue du noeud associé au texte de cours pointe vers le noeud associé à l'index.

"""
import neo4j

def exec(self):
    """
    Exécution des requêtes spécifques de maintenance de la base.
    - récupérer des noeuds textes de cours (maths) dans la base
    - afficher les textes de cours sans noeud associé. La création du noeud n'est pas automatisée.
    - afficher les noeuds Cours sans texte local associé. La suppression du noeud n'est pas automatisée.
    - assurer la cohérence entre les indexations locales et les relations dans le graphe. fonction `indexe()`.

    #### Renvoie

    log: str journal

    """
    print("coucou de exec() dans bdg_mathCours.py")
    
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)

    driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
    
    loc_indexations = self.specific_results['indexations']
    loc_titres = self.specific_results['titres']
    blabla = "\n Titres des textes de cours locaux: {0}"
    print(blabla.format(len(loc_titres)))
    #print(loc_titres)
    
    # noeuds textes de cours (maths)
    param = {'label' : "Document", 
             'propsF' :'{typeDoc:"cours", discipline:"mathématique"}', 
             'propsR' : 'substring(n.urlSrc,51), n.titre'}
    req = self.format_cypher_RETURN(param)
    with driver.session(database="neo4j") as session:
        rem_cours = session.execute_read(self.do_cypher_tx, req)
    blabla = "\n Titres des noeuds textes de cours: {0}"
    print(blabla.format(len(rem_cours)))
    rem_cours.sort(key=lambda paire: paire[0])
    #print(rem_cours)
    
    # Nbs de textes de cours
    blabla = "\n Nbs de textes de cours. local: {nloc},  base: {nrem}"
    blabla = blabla.format(
        nloc= len(loc_titres), nrem=len(rem_cours))
    print(blabla)

    # Cours local sans noeud associé
    loc_orphs = []
    for paire in loc_titres:
        if paire not in rem_cours:
            loc_orphs.append(paire)
    blabla = "\n Fichiers Cours sans noeud distant (à créer) : {0}"
    print(blabla.format(len(loc_orphs)))
    print(loc_orphs)

    # Noeuds Cours isolés (orphelins)
    rem_orphs = []
    for paire in rem_cours:
        if paire not in loc_titres:
            rem_orphs.append(paire)
    blabla = "\n Noeuds Cours sans Cours local (à supprimer) : {0}"
    print(blabla.format(len(rem_orphs)))
    print(rem_orphs)

    # indexations
    indexe(self,loc_indexations)

    driver.close()

    log = ""
    return log

def indexe(self, loc_indexations):
    '''
    Maintient la cohérence entre les relations `INDEXE` de la base en graphe et les indexations locales du dépôt.
    
    Plusieurs listes interviennent
    
    - `loc_indexations` : liste des indexations locales. Une indexation est une paire (fichier, litteral). Elle est formée par la fonction `get_liste_indexations` du module [`scantex`](/maintenance/scantex.html).
    - `rem_concepts`: liste des littéraux des concepts dans la base en graphe.
    - `rem_indexations`: Liste des indexations dans la base en graphe. Une indexation est une paire (fichier, litteral). Le fichier est une propriété d'un noeud `Document` de type `Cours` qui indexe un `Concept'. Le litteral de ce concept est le deuxième élément de la paire.
    
    Que fait cette fonction ?
    
    1. Parcourir `loc_indexations` en examinant le litteral de chaque paire pour partitionner en 3 sous listes à afficher.
        - `loc_index_orphs`: indexations locales sans noeud Concept associé. Créer les noeuds Concepts associés.
        - `loc_index_orphs_spec`: indexations locales spéciales sans noeud Concept associé. Elles servent à organiser les index dans le rendu pdf du fichier. Elles contiennent des "!" et je ne sais pas trop quoi en faire pour le moment.
        - `loc_index_concept`: indexations locales associées à un noeud Concept. (avec ou sans arête `INDEXE`) les créer si besoin.
    
    2. Parcourir les paires de `loc_index_orphs`
        - créer un noeud concept de même litteral que la paire.
        - supprimer la paire de `loc_index_orphs`
        - ajouter la paire à `loc_index_concept`.
    
    3. Parcourir les paires de `loc_index_concept`
        - placer dans `loc_index_concept_orphs` les paires qui ne sont pas dans `rem_indexations`.
    
    4. Parcourir les paires de `loc_index_concept_orphs`
        - créer dans la base une relation `INDEXE` entre le noeud `Document` associé au fichier et le noeud `Concept` associé au litteral.


    '''
    print("\n coucou de indexe()")
    data = self.connect_data
    URI = data['credentials']['URI']
    user = data['credentials']['user']
    password = data['credentials']['password']
    AUTH = (user, password)

    driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
    
    # Formation de loc_indexations. Elle est passée en paramètre, formée dans le module scantex
    # Elimination des doublons (les listes de 2 ne sont pas hashables)
    loc_indexations_tuple = list(map(tuple,loc_indexations))
    loc_indexations_tuple = list(set(loc_indexations_tuple))
    loc_indexations = list(map(list,loc_indexations_tuple))
    print("\n Indexations locales: {0}".format(len(loc_indexations)))
    #print(loc_indexations)

    # Formation de rem_concepts: liste des noeuds concepts dans le graphe
    param = {'label' : "Concept",
             'propsF' :'{ }',
             'propsR' : ' n.litteral'}
    req = self.format_cypher_RETURN(param)
    with driver.session(database="neo4j") as session:
        rem_concepts = session.execute_read(self.do_cypher_tx, req)
    print("\n Libellé des noeuds concepts:{0}".format(len(rem_concepts)))
    rem_concepts.sort()
    #print(rem_concepts)
    
    # Formation de `rem_indexations`: liste des indexations dans la base en graphe.
    # Arêtes "INDEXE" dans le graphe
    req = ''' MATCH (p:Document {typeDoc:"cours"}) -[:INDEXE]-> (c:Concept)
    RETURN replace(substring(p.url,62),".pdf",""), c.litteral
    '''
    #print(req) session.execute_write ??
    with driver.session(database="neo4j") as session:
        rem_indexations = session.execute_read(self.do_cypher_tx, req)
    blabla ="\n Arêtes `INDEXE` dans le graphe: {}"
    print(blabla.format(len(rem_indexations)))
    #print(rem_indexations)

    # 1. Parcours de loc_indexations pour former les 3 listes
    loc_index_orphs = []
    loc_index_orphs_spec = []
    loc_index_concept = []
    for paire in loc_indexations:
        if [paire[1]] not in rem_concepts:
            if "!" in paire[1]:
                loc_index_orphs_spec.append(paire)
            else:
                loc_index_orphs.append(paire)
        else:
            loc_index_concept.append(paire)

    blabla = "\n Indexations locales spéciales sans noeud concept; {0}"
    print(blabla.format(len(loc_index_orphs_spec)))
    print(loc_index_orphs_spec)

    blabla = "\n Indexations locales sans noeud concept (à créer): {0}"
    print(blabla.format(len(loc_index_orphs)))
    print(loc_index_orphs)

    # 2. Parcours de loc_index_orphs pour créer les concepts - changement de liste
    print("création des concepts ...")
    propsF = 'litteral: "{0}", '
    propsF += 'date: datetime(), '
    propsF += 'typeConcept: "index Latex", '
    propsF += 'discipline: "mathématique"'
    param = {'label' : "Concept"}
    print("\n")
    for paire in loc_index_orphs:
        param['propsF'] = "{" + propsF.format(paire[1]) + "}"
        # print(param)
        req = self.format_cypher_CREATE(param)
        with driver.session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req)
        # changement de liste
            # supprimer paire de loc_index_orphs
        loc_index_orphs.remove(paire)
            # ajouter paire à loc_index_concept
        loc_index_concept.append(paire)
    blabla = "\n Indexations locales avec noeud concept: {0}"
    print(blabla.format(len(loc_index_concept)))

    # 3. Parcourir les paires de loc_index_concept pour trouver les relations `INDEXE` manquantes dans le graphe
    loc_index_concept_orphs = []
    for paire in loc_index_concept:
        if paire not in rem_indexations:
            loc_index_concept_orphs.append(paire)
    blabla = "\n Indexations locales avec noeud concept sans arête `INDEXE`: {0}"
    print(blabla.format(len(loc_index_concept_orphs)))
    print(loc_index_concept_orphs)

    # 4. Parcourir les paires de loc_index_concept_orphs pour créer les arêtes `INDEXE` manquantes dans le graphe.
    req = '''
    MATCH (p:Document), (c:Concept)
    WHERE p.typeDoc = "cours"
        AND c.typeConcept = "index Latex"
        AND replace(substring(p.url,62),".pdf","") = "{0}"
        AND c.litteral = "{1}"
    CREATE (p) -[:INDEXE]-> (c)
    '''
    print("création des arêtes ...")
    for paire in loc_index_concept_orphs:
        req1 = req.format(paire[0],paire[1])
        print(req1)
        with driver.session(database="neo4j") as session:
            val = session.execute_write(self.do_cypher_tx, req1)

    driver.close()
