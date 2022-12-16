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
    ]

# module spécifique
execloc_module = 'exl_mathPbs'

# publish_data : fichiers à publier
publish_data = {
    'patterns': ['pdfdir/A_*.pdf', 'htmldir/*'],
    # 'liste': ['A_'],
    'uri_esp': 'https://maquisdoc-math.fra1.digitaloceanspaces.com/'}

# dp pour dépôt
dp_data = {'nom': 'math-pbs',
           'relative_path': '../math-pbs/',
           'execloc_module': execloc_module,
           'execloc_data': execloc_data,
           'publish_data': publish_data}


#   #################       ZONE SECRETE   #################
#       paramètres de connexion à l'espace (de publication web)
sp_connect_data = {'region_name': 'fra1',
                   'endpoint_url': 'https://fra1.digitaloceanspaces.com',
                   'bucket': 'maquisdoc-math',
                   'prefix': 'math-pbs/'}
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
