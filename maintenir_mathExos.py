# -*- coding: utf-8 -*-
"""
Maintenir le dépôt `math-exos`.

Modifié le 09/03/23  @author: remy

  - Importe [`init_mathExos`](init_mathExos.html) qui code le *manifeste*
  du dépôt.
  - Importe [`depot`](depot.html) qui définit la classe `Depot`.
  - Instancie un objet `Depot` ce qui effectue la maintenance.
  - Affiche la propriété `.journal` de l'objet `Depot`.

Le manifeste d'un dépôt décrit
- ses conventions d'organisation
- son insertion dans les espaces de publication
- son reflet dans la base en graphe de contextualisation

"""
import init_mathExos as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    # INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.manifeste)
    journal = dp.log

    print(journal)
