"""
Package `Maintenance`. Maintient les dépôts maquisdoc.

Modifié le 14/02/23 @author: remy

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
dépôt(GitHub). Les scripts et modules de maintenance ne sont pas encore implémentés pour tous les dépôts. Actuellement:

|Nom dossier local | Nom dépôt(GitHub) | Nom du script de maintenance |
| ---------------- | ----------------- | --------------------------- |
|math-exos         | [math-exos](https://github.com/nicolair/math-exos) | [`maintenir_mathExos`](maintenance/maintenir_mathExos.html)|
|math-pbs          | [math-pbs](https://github.com/nicolair/math-pbs) | [`maintenir_mathPbs`](maintenance/maintenir_mathPbs.html)|
|math-cours        | [math-cours](https://github.com/nicolair/math-cours) | à faire |
|math-rapidexos    | [math-cours](https://github.com/nicolair/math-rapidexos) | à faire |

Le script de maintenance importe des sous-modules spécifiques ainsi que des sous-modules communs.

Par exemple, les sous-modules dont le nom se termine par `_mathExos` sont
spécifiques au dépôt d'exercices `math-Exos`.

Sur la machine de travail de l'auteur, un dépôt est un sous-dossier
de `maquisdoc-depots` dont le nom contient un tiret '-'.
En python, les noms de modules ne doivent pas contenir de tiret. Les noms des
modules spécifiques sont formés en passant du tiret à la majuscule dans le
nom du dépôt. Exemple `init_mathExos` et `exl_mathExos`.
dans lesquels `math-exos` a été changé en `mathExos`.

La maintenance utilise des modules externes à la bibliothèque Python standard. La gestion de l'environnement virtuel et des dépendances est assuré par [Poetry](https://python-poetry.org/docs/).  
Exemples de commande:
- `poetry install` pour installer localement les dépendances du projet définies dans `pyproject.toml` 
- `poetry run python ./maintenir_mathExos.py` pour lancer la maintenance du dépôt
 d'exercice
- `poetry run pdoc ../maintenance.py -o ./docs` pour lancer la création de cette
 documentation.

La maintenance d'un dépôt est lançée par le script indiqué dans le tableau précédent. Il importe d'abord le module spécifique d'initialisation (son nom commence par `init_`) représentant le *manifeste* du dépôt. Il importe ensuite des modules communs ainsi que d'autres modules spécifiques. Les différents types de modules et les classes définies sont précisés dans le paragraphe suivant. La maintenance du dépôt des problèmes est détaillée.

####  Modules et classes
Les modules importés lors d'une maintenance sont de différents types.

<div style="text-align: center;">
  Modules locaux communs
</div>

| nom           | rôle             | importe |
| ------------- | ---------------- | --------- |
| `depot`       | [module principal](maintenance/depot.html) | `execlocal`, `espace`, `graphdb` |
| `execlocal`   | [définit la classe `Execlocal`](maintenance/execlocal.html) | `scantex`, `exl_` spécifique |
| `scantex`     | [outils d'analyse de fichiers .tex](maintenance/scantex.html) |     |
| `espace`      | [definit la classe `Espace`](maintenance/espace.html) |     |
| `graphdb`     | [définit la classe `Maquis`](maintenance/graphdb.html) | `bdg_` spécifique |



<div style="text-align: center; margin-top: 5px;">
  Modules locaux spécifiques
</div>

| nom            | rôle                       |
| -------------- | -------------------------- |
| `init_mathPbs` | [initialisation, manifeste](maintenance/init_mathPbs.html) |
| `exl_mathPbs`  | [scripts de manipulation de fichiers locaux](maintenance/exl_mathPbs.html) |
| `bdg_mathPbs`  | [manipulation de données de la base en graphe](maintenance/bdg_mathExos.html) |
| `init_mathExos` | [initialisation, manifeste](maintenance/init_mathExos.html) |
| `exl_mathExos` | [scripts de manipulation de fichiers locaux](maintenance/exl_mathExos.html) |


<div style="text-align: center; margin-top: 5px;">
  Modules de la bibliothèque Python
</div>

| nom          | rôle  |
| -----------  | ----- |
| `os`         | [Operating system interface](https://docs.python.org/3.11/library/os.html#module-os) |
| `sys`        | [System-specific parameters and functions](https://docs.python.org/3.11/library/sys.html?highlight=sys#module-sys) |
| `importlib`  | [The implementation of import](https://docs.python.org/3.11/library/importlib.html?highlight=importlib#module-importlib) |
| `subprocess` | [Subprocess management](https://docs.python.org/3.11/library/subprocess.html?highlight=subprocess#module-subprocess) |
| `glob`       | [Unix style pathname pattern expansion](https://docs.python.org/3.11/library/glob.html)|
| `os.path`    | [Common pathname manipulations](https://docs.python.org/3.11/library/os.path.html) |
| `mimetypes`  | [Map filenames to MIME types](https://docs.python.org/3.11/library/mimetypes.html?highlight=mimetypes#module-mimetypes) |

<div style="text-align: center; margin-top: 5px;">
  Modules externes
</div>
| nom          | rôle  |
| -----------  | ----- |
| `boto3`      |[client de l'API d'un espace](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)|
| `neo4j`      |[client de l'API de la base de données en graphe (neo4j)](https://neo4j.com/docs/api/python-driver/current/)|
|`pdoc`        |[génération de cette documentation](https://pdoc.dev/docs/pdoc.html)|


Les modules définissent diverses classes. Ce sont les instanciations de ces classes qui effectuent les différentes tâches de la maintenance.

<div style="text-align: center;">
  Classes
</div>

| nom         | module      | rôle |
| ----------- | ----------- | ----- |
| `Depot`     | `depot`     | instancie les 3 classes suivantes |
| `Execlocal` | `execlocal` | interface avec le dossier local du dépôt  |
| `Espace`    | `espace`    | interface avec l'espace Digital Ocean |
| `Maquis`    | `graphdb`   | interface avec la base en graphe neo4j |

####  Exemple avec *math-pbs*
La maintenance est lancée par la commande

    python3 maintenir_mathPbs

dans le dossier contenant le script.

Ce script importe les modules `init_mathPbs` et `depot` puis instancie un objet `Depot`.  
Le module `depot` importe les modules `execlocal`, `espace` et `graphdb`.  
L'initialisation de l'instance de `Depot` instancie
- un objet `Execlocal`
- un objet `Espace`
- un objet `Maquis`

L'instanciation de l'objet `Execlocal` met à jour le dossier local.

L'instanciation de l'objet `Espace` met à jour l'espace associé au dépôt.

> Le module `boto3` fournit un client Python pour l'API de l'espace.  
> Les credentials d'accès à un espace sont des clés générées à partir de l'interface Digital Ocean. Ces clés sont stockées localement dans le fichier `~/.aws/credentials` auquel accède silencieusement le client `boto3`.


L'instanciation de l'objet `Maquis` met à jour la partie de la base en graphe associée au dépôt.

> Le module `neo4j` fournit un client Python pour l'API de la base en graphe.  
> Les credentials d'accès à la base (user, password) sont récupérés (`sp_connect_data`) à partir de variables d'environnement lors de l'importation de `init_mathPbs`.


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
    "bdg_mathPbs",
    "depot",
    "execlocal",
    "scantex",
    "espace",
    "graphdb"
    ]

