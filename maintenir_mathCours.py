# -*- coding: utf-8 -*-
"""
Modifié le 30/03/23  @author: remy

Maintenir le dépôt `math-cours`.

- Importe [`init_mathCours`](init_mathCous.html) qui code le *manifeste* du
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
