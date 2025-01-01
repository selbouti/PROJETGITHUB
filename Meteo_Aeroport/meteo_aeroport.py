import argparse  # Pour gérer les arguments de la ligne de commande
import json  # Pour manipuler les fichiers JSON
from datetime import datetime
from module_projet import recuperer_donnees_metar_taf, recuperer_donnees_meteobleu, get_code_aeroport
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Route pour la page principale (HTML)
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

# Route pour récupérer les données météo en format JSON
@app.route('/Meteo_Aeroport/donnees_meteo.json', methods=['GET'])
def main():
    """
    Fonction principale qui gère l'exécution du script.
    """
    # Configuration des arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Extrait les données météo d'un aéroport et génère un fichier JSON pour la page web.")
    parser.add_argument(
        "-a", "--aeroport",
        required=True,
        help="Code ou nom de l'aéroport (ex: 'LFPG' pour Charles de Gaulle)."
    )
    parser.add_argument(
        "-d", "--day",
        type=int,
        default=0,
        help="Numéro du jour pour la prévision (0 pour aujourd'hui, 1 pour demain, etc.)."
    )
    parser.add_argument(
        "-o", "--output",
        default="../html/donnees_meteo.json",
        help="Nom du fichier de sortie pour les données extraites (par défaut: donnees_meteo.json)."
    )

    args = parser.parse_args()

    # Récupérer les données METAR et TAF
    print(f"Récupération des données METAR/TAF pour {args.aeroport}...")
    metar_taf_data = recuperer_donnees_metar_taf(get_code_aeroport(args.aeroport))
    
    # Récupérer les données de prévision météo
    print(f"Récupération des données de prévision pour le jour {args.day}...")
    argument_nom = 'aéroport-{args.aeroport.replace}_france_6269554'
    meteobleu_data = recuperer_donnees_meteobleu(argument_nom, args.day)

    # Fusionner les données METAR/TAF et prévisions
    all_data = metar_taf_data if metar_taf_data else {}
    if meteobleu_data:
        all_data.update(meteobleu_data)

    # Ajouter la date et l'heure d'extraction
    all_data['date_extraction'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sauvegarder les données dans un fichier JSON
    print(f"Sauvegarde des données dans {args.output}...")
    with open(args.output, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    print("Données extraites et sauvegardées avec succès.")

if __name__ == "__main__":
    main()
