# -*- coding: utf-8 -*-
"""
Outils d'analyse de fichiers sources ou produits par LateX.

Modifié le 22/01/23  @author: remy

Travaille dans le répertoire courant c'est à dire celui du dépôt à maintenir.'
"""
import os
import glob

def get_date_srce(nom):
    """
    Renvoie une date de source.

    Fonction récursive.
    
    - Si le fichier ne contient ni input ni includegraphics,
        - renvoie la date de maj du fichier.
    - Sinon
         - renvoie la date la plus récente entre sa date de maj et celle
            des input et includegraphics.
    """
    try:
        date_srce = os.path.getmtime(nom)
    except FileNotFoundError:
        print(nom, ' pas trouvé')
        date_srce = 0

    # date des sources tex inputtés
    liste = get_liste_inputs(nom)
    for fic in liste:
        t = get_date_srce(fic)
        # print(fic,t)
        if t > date_srce:
            date_srce = t

    # date des figures et des lignes de code incluses
    liste = get_liste_includegraphics(nom) + get_liste_lstinputlistings(nom)
    for fic in liste:
        try:
            t = os.path.getmtime(fic)
        except FileNotFoundError:
            print('Erreur : ', fic, ' pas trouvé')
            t = 0
        # print(fic, t)
        if t > date_srce:
            date_srce = t
    return date_srce


def get_liste_inputs(nom):
    """Renvoie la liste des sources tex dans des input."""
    fifi = open(nom, 'r')

    text = fifi.read()
    long = len(text)
    inputs = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\input{', cc, long)
        if c != -1:
            c += 7
            cc = text.find('}', c, long)
            nominput = text[c:cc]
            if '.' not in nominput:
                nominput += '.tex'
            if nominput not in inputs:
                inputs.append(nominput)
    return inputs


def get_liste_includegraphics(nom):
    """Renvoie la liste des figures (pdf) dans des includegraphics."""
    fifi = open(nom, 'r')
    text = fifi.read()
    long = len(text)
    includes = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\includegraphics', cc, long)
        if c != -1:
            # il peut y avoir une option '[width= ]'
            c = text.find('{', c, long)
            c += 1
            cc = text.find('}', c, long)
            fig = text[c:cc]
            # si pas d'extension on place .pdf
            if not os.path.splitext(fig)[1]:
                print('extension pdf manque dans', nom)
                fig += '.pdf'
            if fig not in includes:
                includes.append(fig)
    return includes


def get_liste_lstinputlistings(nom):
    """
    Renvoie une liste des fichiers.

    Ceux contenant des lignes de codes insérées par `lstinputlisting`.
    """
    fifi = open(nom, 'r')
    text = fifi.read()
    long = len(text)
    lstinputs = []
    c, cc = 0, 0  # compteurs dans la chaine de caractère
    while c != -1:
        c = text.find('\\lstinputlisting', cc, long)
        if c != -1:
            # il y a une option '[width= ] à sauter'
            c = text.find('{', c, long)
            c += 1
            cc = text.find('}', c, long)
            lstinput = text[c:cc]
            # si pas d'extension on place .py
            if not os.path.splitext(lstinput)[1]:
                print('extension pdf manque dans', nom)
                lstinput += '.py'
            if lstinput not in lstinputs:
                lstinputs.append(lstinput)
    return lstinputs


def aexec(src):
    """Renvoie `Vrai` si un `input` plus récent que le `.pdf`."""
    ext = os.path.splitext(src)[1]
    img = src.replace(ext, '.pdf')
    # print(img)
    date_img = 0
    date_src = get_date_srce(src)
    if os.path.exists(img):
        date_img = os.path.getmtime(img)
    return date_src > date_img


def acompiler(src, img):
    """
    Renvoie `Vrai` si `src` est à compiler.

    C'est à dire si un `input` de la source est plus récent que l'image.

    #### Parameters
    
    - src : .
    - img : chaine de caractère représentant le nom du fichier image.

    #### Returns

    None.

    """
    # imgext = os.path.splitext(img)[1]
    # print(img)
    date_img = 0
    date_src = get_date_srce(src)
    if os.path.exists(img):
        date_img = os.path.getmtime(img)
        # if imgext == '.html':
        #    print(img, date_src > date_img)

    return date_src > date_img

def get_liste_indexations(path_pattern):
    """
    Renvoie la liste des indexations.
    
    Examine les fichiers .idx créés par la commande d'indexation lors de la
    compilation.
    
    #### Paramètres
    
    `path_pattern`: str,  pattern de la chaine de caractère des chemins des fichiers
    idx d'index.'  
    Exemple `auxdir/A*.idx`.
    
    #### Returns
    
    Une liste de couples `[nomfic, litteral]` où
    - `nomfic` est un nom de fichier .tex
    - `litteral` est une chaine de caractères indexée dans `nomfic`. 
    """
    
    indexations = []
    idxpaths = glob.glob("auxdir/A*.idx")
    for idxpath in idxpaths:
        doc = os.path.basename(idxpath)
        doc = doc.removeprefix('A')
        doc = doc.removesuffix(('.idx'))
        f = open(idxpath)
        for line in f:
            line = line.removeprefix('\\indexentry{')
            i = line.find('|hyperpage')
            line = line[0:i]
            indexations.append([doc,line])
        f.close()
    # print(indexations)
    return indexations

def get_liste_descriptions(description_pattern):
    """
    Renvoie la liste des descriptions.
    

    #### Parametres
    description_pattern : dictionnaire 
        {
            'path_pattern': pattern des chemins des fichiers à examiner,
            'tags': paire de balises entourant la description
        }

    #### Renvoie
    
    Liste de couples ['nom du document', 'description de document']

    """
    descriptions = []
    path_pattern = description_pattern['path_pattern']
    tags = description_pattern['tags']
    nomfics = glob.glob(path_pattern)
    for nomfic in nomfics:
        file = open(nomfic)
        fictex = file.read()
        file.close()
        if i:= fictex.find(tags[0]) >= 0:
            i += len(tags[0]) - 1
            j = fictex.find(tags[1]) 
            nomfic = nomfic.removeprefix(path_pattern[0])
            nomfic = nomfic.removesuffix('.tex')
            descriptions.append([nomfic,fictex[i:j]])
    return descriptions