# -*- coding: utf-8 -*-
"""
Maintenir le dépôt `math-exos`.

Modifié le 06/01/23  @author: remy

  - Importe [`init_mathExos`](init_mathExos.html) qui code le *manifeste*
  du dépôt.
  - Importe [`depot`](depot.html) qui définit la classe `Depot`.
  - Instancie une classe `Depot` ce qui effectue la maintenance.
  - Affiche la propriété `.journal` de l'objet `Depot`.


Le manifeste d'un dépôt est la description des conventions d'organisation
d'un dépôt.

"""
import init_mathExos as init_DPT
import depot

if __name__ == '__main__':
    journal = {}

    # INSTANCIATION d'un objet Depot
    dp = depot.Depot(init_DPT.para)
    journal = dp.log

    print(journal)
