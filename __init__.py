"""
Package `Maintenance`. Maintient des dépôts maquisdoc.

Modifié le 31/01/23 @author: remy

Attention dans cette documentation, le terme 'dépôt' désigne une composante
du projet maquisdoc. On utilisera 'dépot (GitHub)' pour désigner un dépôt
hébergé par GitHub. Par exemple, ce package est un dépot (GitHub)
[mtn-dpt](https://github.com/nicolair/mtn_dpt).

La maintenance assure la cohérence entre l'état local d'un dépôt dans lequel un
 auteur vient de travailler et les autres composantes du projet.

Le rôle de la maintenance est de :

* pousser les modifications locales vers le dépôt en ligne
 (un dépôt maquisdoc est un dépôt GitHub).
* compiler localement les images qui doivent l'être.
* pousser vers les espaces de diffusion les images nouvelles ou modifiées.
* mettre à jour la base de données en graphe.

Chaque dépôt est un dossier de la machine de travail de l'auteur et un
dépôt(GitHub). Actuellement:

|Nom dossier local | Nom dépôt(GitHub) | Nom du script de maintenance |
| ---------------- | ----------------- | --------------------------- |
|math-exos         | [math-exos](https://github.com/nicolair/math-exos) | [`maintenir_mathExos`](maintenance/maintenir_mathExos.html)
|math-pbs          | [math-pbs](https://github.com/nicolair/math-pbs) | [`maintenir_mathPbs`](maintenance/maintenir_mathPbs.html)

Le script de maintenance importe des sous-modules spécifiques ainsi que des
 sous-modules communs.

Par exemple, les sous-modules dont le nom se termine par `_mathExos` sont
spécifiques au dépôt d'exercices `math-Exos`.

Sur la machine de travail de l'auteur, un dépôt est un sous-dossier
de `maquisdoc-depots` dont le nom contient un tiret '-'.
En python, les noms de modules ne doivent pas contenir de tiret. Les noms des
modules spécifiques sont formés en passant du tiret à la majuscule dans le
nom du dépôt. Exemple `init_mathExos` et `exl_mathExos`.
dans lesquels `math-exos` a été changé en `mathExos`.

La maintenance utilise des bibliothèques Python externes comme clients des
API des espaces Digital Ocean et de la base neo4j.

- boto3 pour les espaces
- ??? pour neo4j

Ils sont installés dans un environnement virtuel géré par `Poetry`.
Exemples de commande:
- `poetry run ./maintenir_mathExos.py` pour lancer la maintenance du dépôt
 d'exercice
- `poetry run pdoc ../maintenance` pour lancer la création de cette
 documentation.
"""

import os
import sys

# pour permettre l'import programmatique
localpath = os.path.dirname(__file__)
if localpath not in sys.path:
    sys.path.append(os.path.dirname(__file__))

__all__ = [
    "maintenir_mathExos",
    "maintenir_mathPbs",
    "init_mathExos",
    "init_mathPbs",
    "exl_mathExos",
    "exl_mathPbs",
    "depot",
    "execlocal",
    "scantex",
    "espace",
    "graphdb"
    ]

