# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 11:06:36 2018

@author: remy
"""
# import glob , fnmatch, shutil , os

#                   paramètres du dépôt
# fichiers à exécuter localement
execloc_data = [
    {'ext': '.tex', 'patterns': ['A_*.tex'],
     'imgdir': 'pdfdir/', 'imgext': '.pdf',
     'command': ["latexmk", "-pdf", "-emulate-aux-dir",
                 "-auxdir=auxdir", "-outdir=pdfdir"]},
    {'ext': '.asy', 'patterns': ['*_fig.asy'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["asy", "-f", "pdf"]},
    {'ext': '.py', 'patterns': ['*_fig.py'],
     'imgdir': '', 'imgext': '.pdf',
     'command': ["python3"]},
    {'ext': '.tex', 'patterns': ['Aexo_*.tex'],
     'imgdir': 'htmldir/', 'imgext': '.html',
     'command': ['make4ht', '-u', '-d', 'htmldir']}
    ]

# module spécifique
execloc_module = 'exl_mathExos'

# publish_data : fichiers à publier
publish_data = {
    'patterns': ['pdfdir/A_*.pdf', 'htmldir/*'],
    # 'liste': ['A_'],
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'}

# dp pour dépôt
dp_data = {'nom': 'math-exos',
           'relative_path': '../math-exos/',
           'execloc_module': execloc_module,
           'execloc_data': execloc_data,
           'publish_data': publish_data}


#   #################       ZONE SECRETE   #################
#       paramètres de connexion à l'espace (de publication web)
sp_connect_data = {'region_name': 'fra1',
                   'endpoint_url': 'https://fra1.digitaloceanspaces.com',
                   'bucket': 'maquisdoc-math',
                   'prefix': 'math-exos/'}
#      paramètres de connexion à la base de données en graphe
# local
# bdg_data = {'url' : 'bolt://localhost:7687', 'user': "neo4j", 'pw':"3128"}
# graphenedb
bdg_connect_data = {}
# bdg_connect_data = {
#    'uri' : "bolt://hobby-emmpngdpepmbgbkeiodbecbl.dbs.graphenedb.com:24786",
#    'user': "mimi", 'pw': "b.qzcs8g8XgxeB.Sbc5iAoGjwGi60fr"}
# ###########   FIN DE ZONE SECRETE    ###################


# paramètres de la maintenance
para = {'depot': dp_data, 'espace': sp_connect_data, 'bdg': bdg_connect_data}
