import os
import sys
sys.path.insert(0, os.path.abspath('chemin//du/repertoire/ou/sont/les/fonctions'))`

Exemple :
`import os
import sys
sys.path.insert(0, os.path.abspath('../../statistiques-connexions-apache'))`

avec dans le répertoire mes fonctions et le fichier main :

statistiques-connexions-apache/
├── camenbert_navigateur.py
├── config.py
├── extraction_navigateur.py
├── histogramme_connexions_mois.py
├── histogramme_connexions_sem.py
├── html_generator.py
├── __init__.py
├── main.py
├── nombres_total_requetes.py


