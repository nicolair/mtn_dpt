# -*- coding: utf-8 -*-
"""
Modifié le 18/12/23  @author: remy

Maintenir le dépôt `math-cours`.

Commande de lancement

      poetry run python ./maintenir_mathCours.py

- Importe [`init_mathCours`](init_mathCours.html) qui code le *manifeste* du
  dépôt.
- Instancie un objet `Depot` ce qui effectue la maintenance.
- Affiche la propriété `.journal` de l'objet `Depot`.


Le manifeste d'un dépôt décrit
- ses conventions d'organisation
- son insertion dans les espaces de publication
- son reflet dans la base en graphe de contextualisation

"""
import init_mathCours as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    #                        INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.manifeste)
    journal = dp.log

    print(journal)
