# -*- coding: utf-8 -*-
"""
Modifié le 09/03/23  @author: remy

Maintenir le dépôt `math-pbs`.

- Importe [`init_mathPbs`](init_mathPbs.html) qui code le *manifeste* du
  dépôt.
- Instancie un objet `Depot` ce qui effectue la maintenance.
- Affiche la propriété `.journal` de l'objet `Depot`.


Le manifeste d'un dépôt décrit
- ses conventions d'organisation
- son insertion dans les espaces de publication
- son reflet dans la base en graphe de contextualisation

"""
import init_mathPbs as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    #                        INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.manifeste)
    journal = dp.log

    print(journal)
