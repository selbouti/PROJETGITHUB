
import requests  # type: ignore # Pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # type: ignore # Pour analyser le contenu HTML
import re  # Pour les expressions régulières
from datetime import datetime  # Pour manipuler les dates
import json  # Pour manipuler les fichiers JSON

def get_html_page(url):
    """
    Récupère le contenu HTML d'une page web à partir de son URL.

    Args:
        url (str): L'URL de la page web.

    Returns:
        BeautifulSoup: Objet BeautifulSoup contenant le contenu HTML.
    """
    try:
        entete = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=entete)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return None

def recuperer_donnees_meteobleu(site_aeroport, number):
    """
    Extrait les données météo d'une page MeteoBleu.

    Args:
        site_aeroport (str): Code ou nom de l'aéroport.
        number (int): Numéro du jour.

    Returns:
        dict: Dictionnaire contenant les données extraites.
    """
    url = f"https://www.meteoblue.com/fr/meteo/semaine/{site_aeroport}?day={number}"
    
    soup = get_html_page(url)
        

    div = soup.find('div', id=f'day{number}')
    tab = div.find_next('div', class_='tab-content')
    if div:
        temperature_max = tab.find('div', class_='tab-temp-max').get_text(strip=True) if tab.find('div',class_="tab-temp-max") else None
        temperature_min = tab.find('div',class_="tab-temp-min").get_text(strip=True) if div.find('div',class_="tab-temp-min") else None
        precipitation = tab.find('div',class_="tab-precip").get_text(strip=True) if div.find('div',class_="tab-precip") else None
        wind_div = tab.find('div',class_="wind")
        vent_vitesse = tab.find('div',class_="wind").get_text(strip=True) if wind_div and tab.find('div',class_="wind") else None
        vent_direction = wind_div.find('span')['class'][2] if wind_div and wind_div.find('span')['class'][2] else None
        ensoleillement = tab.find(class_="tab-sun").get_text(strip=True) if div.find(class_="tab-sun") else None
        return {
            "temperature_max": temperature_max.replace('\xa0', ' '),
            "temperature_min": temperature_min.replace('\xa0', ' '),
            "precipitation": precipitation,
            "vent_vitesse": vent_vitesse,
            "vent_direction": direction_vent_meteobleu(vent_direction),
            "ensoleillement": ensoleillement
        }
    else:
        print(f"Div avec id=day {number} introuvable.")
        return None
def direction_vent_meteobleu(wind_direction):
    # Dictionnaire des directions de vent
    directions = {
        "S": "Sud",
        "SW": "Sud-Ouest",
        "W": "Ouest",
        "NW": "Nord-Ouest",
        "N": "Nord",
        "NE": "Nord-Est",
        "E": "Est",
        "SE": "Sud-Est"
    }
    
    # Retourner la direction complète à partir de l'abréviation
    return directions.get(wind_direction, "Direction inconnue")

def recuperer_donnees_metar_taf(code_aeroport):
    """
    Extrait les données METAR/TAF d'une page.

    Args:
        code_aeroport (str): Code de l'aéroport (ICAO ou autre).

    Returns:
        dict: Dictionnaire contenant les données extraites.
    """
    url = f"https://metar-taf.com/fr/{code_aeroport}"

    soup = get_html_page(url)
    
    data = {}
    metar_div = soup.find('div', id='metar')
    if metar_div:
        # Nom de l'aéroport
        airport_name_match =re.search(r'<h1 class="h4 mb-0 text-ellipsis">(.+?)</h1>', str(metar_div))
        data['airport_name'] = airport_name_match.group(1).strip() if airport_name_match else None

        # Température
        temp_match = re.search(r'(\d+ \u00b0C)', str(metar_div))
        data['temperature'] = temp_match.group(1).strip() if temp_match else None

        # Visibilité
        visibility_match = re.search(r'<h3 class="mb-0">(\d+ km)</h3>', str(metar_div))
        data['visibility'] = visibility_match.group(1).strip() if visibility_match else None

        # Vitesse et direction du vent
        wind_speed_match = re.search(r'<h3 class="mb-0">\s*(\d+\s*kt)\s*</h3>', str(metar_div))
        wind_dir_match = re.search(r'(\d{3}\u00b0)', str(metar_div))
        data['wind_speed'] = (wind_speed_match.group(1).strip()) if wind_speed_match else None
        data['wind_direction'] = wind_dir_match.group(1).strip() if wind_dir_match else None

        # Altitude des nuages
        cloud_alt_match = re.search(r'<h3 class="mb-0">s*(\d+(\.\d+)?)\s*ft\s*</h3>', str(metar_div))
        data['cloud_altitude'] = cloud_alt_match.group(1).strip() if cloud_alt_match else None

        # Pression atmosphérique
        pressure_match = re.search(r'<h3 class="mb-0">(\d+ hPa)</h3>', str(metar_div))
        data['pressure'] = pressure_match.group(1).strip() if pressure_match else None
    

    return convertir_donnees_metar(data)

def direction_du_vent_metar(degrees):
    """
    Identifie la direction du vent en fonction de l'angle en degrés.

    Cette fonction prend un angle en degrés (compris entre 0 et 360) et retourne
    la direction du vent correspondant à cet angle selon les directions cardinales
    et intermédiaires.

    Paramètres :
    degrees (float) : L'angle en degrés mesuré par rapport au nord, compris entre 0 et 360.
                      Par exemple, 0° correspond au Nord, 90° à l'Est, 180° au Sud, etc.

    Retourne :
    str : La direction du vent correspondante (par exemple, "Nord", "Sud-Ouest").
          Si l'angle est invalide (en dehors de l'intervalle [0, 360]), la fonction retourne "Direction invalide".

    Exemple :
    >>> direction_du_vent(290)
    'Ouest'
    
    >>> direction_du_vent(45)
    'Nord-Est'
    
    >>> direction_du_vent(400)
    'Direction invalide'
    """
    
    # Créer une liste des intervalles de degrés correspondant aux directions cardinales
    directions = [
        (0, "Nord"),
        (45, "Nord-Est"),
        (90, "Est"),
        (135, "Sud-Est"),
        (180, "Sud"),
        (225, "Sud-Ouest"),
        (270, "Ouest"),
        (315, "Nord-Ouest"),
    ]
    
    # S'assurer que l'angle est dans l'intervalle [0, 360]
    if degrees < 0 or degrees >= 360:
        return "Direction invalide"

    # Trouver la direction correspondant à l'angle
    for i in range(len(directions) - 1):
        if degrees >= directions[i][0] and degrees < directions[i + 1][0]:
            return directions[i][1]
    
    # Si l'angle est supérieur ou égal à 315°, c'est le Nord
    return directions[-1][1]

def convertir_donnees_metar(data):
    """
    Convertit les unités des données météorologiques dans le dictionnaire `data` et 
    met à jour ces valeurs avec les unités mondiales.

    Paramètres :
    data (dict) : Un dictionnaire contenant les données météorologiques avec les unités locales.

    Retourne :
    dict : Le dictionnaire mis à jour avec les données converties et les unités mondiales.
    """

    # Conversion de la vitesse du vent de nœuds (kt) en km/h
    if data.get('wind_speed'):
        data['wind_speed'] = str(float(data.get('wind_speed').replace('kt', '').strip()) * 1.852) + ' km/h'
    
    # Conversion de l'altitude des nuages de pieds (ft) en mètres
    if data.get('cloud_altitude'):
        data['cloud_altitude'] = str(float(data.get('cloud_altitude').replace('ft', '').strip()) * 0.3048) + ' m'
    
    # Conversion de la direction du vent en texte lisible (Nord, Est, etc.)
    if data.get('wind_direction'):
        data['wind_direction'] = direction_du_vent_metar(float(data.get('wind_direction').replace('°', '').strip()))

    return data

def get_code_aeroport (name):
    # Liste des aéroports en France et leurs codes OACI
    aeroports = [
        {"nom": "Paris-Charles-de-Gaulle", "code_oaci": "LFPG"},
        {"nom": "Paris-Orly", "code_oaci": "LFPO"},
        {"nom": "Lyon-Saint-Exupéry", "code_oaci": "LFLL"},
        {"nom": "Marseille-Provence", "code_oaci": "LFML"},
        {"nom": "Nice-Côte d'Azur", "code_oaci": "LFMN"},
        {"nom": "Toulouse-Blagnac", "code_oaci": "LFBO"},
        {"nom": "Bordeaux-Mérignac", "code_oaci": "LFBD"},
        {"nom": "Nantes-Atlantique", "code_oaci": "LFRS"},
        {"nom": "Strasbourg-Entzheim", "code_oaci": "LFST"},
        {"nom": "Lille-Lesquin", "code_oaci": "LFQQ"},
        {"nom": "Montpellier-Méditerranée", "code_oaci": "LFMT"},
        {"nom": "Rennes-Saint-Jacques", "code_oaci": "LFRN"},
        {"nom": "Bâle-Mulhouse (EuroAirport)", "code_oaci": "LFSB"},
        {"nom": "Ajaccio-Napoléon-Bonaparte", "code_oaci": "LFKJ"},
        {"nom": "Bastia-Poretta", "code_oaci": "LFKB"},
        {"nom": "Figari-Sud-Corse", "code_oaci": "LFKF"},
        {"nom": "Clermont-Ferrand Auvergne", "code_oaci": "LFLC"},
        {"nom": "Pau-Pyrénées", "code_oaci": "LFBP"},
        {"nom": "Perpignan-Rivesaltes", "code_oaci": "LFMP"},
        {"nom": "Brest Bretagne", "code_oaci": "LFRB"},
        {"nom": "Deauville-Normandie", "code_oaci": "LFRG"},
        {"nom": "Limoges-Bellegarde", "code_oaci": "LFBL"},
        {"nom": "Toulon-Hyères", "code_oaci": "LFTH"},
        {"nom": "Lorient Bretagne Sud", "code_oaci": "LFRH"},
        {"nom": "Grenoble Alpes Isère", "code_oaci": "LFLS"},
        {"nom": "Caen-Carpiquet", "code_oaci": "LFRK"},
        {"nom": "Le Havre-Octeville", "code_oaci": "LFOH"},
        {"nom": "Angers-Loire", "code_oaci": "LFJR"},
        {"nom": "Tours Val de Loire", "code_oaci": "LFOT"},
        {"nom": "Metz-Nancy-Lorraine", "code_oaci": "LFJL"},
        {"nom": "Dijon-Bourgogne", "code_oaci": "LFSD"},
        {"nom": "Chambéry-Savoie", "code_oaci": "LFLB"},
        {"nom": "Tarbes-Lourdes-Pyrénées", "code_oaci": "LFBT"},
        {"nom": "La Rochelle-Île de Ré", "code_oaci": "LFBH"},
        {"nom": "Poitiers-Biard", "code_oaci": "LFBI"},
        {"nom": "Avignon-Provence", "code_oaci": "LFMV"},
        {"nom": "Nîmes-Alès-Camargue-Cévennes", "code_oaci": "LFTW"},
        {"nom": "Brive-Souillac", "code_oaci": "LFSL"},
        {"nom": "Biarritz-Pays Basque", "code_oaci": "LFBZ"},
        {"nom": "Calvi-Sainte-Catherine", "code_oaci": "LFKC"},
        {"nom": "Agen-La Garenne", "code_oaci": "LFBA"},
        {"nom": "Annecy Mont-Blanc", "code_oaci": "LFLP"},
        {"nom": "Valence-Chabeuil", "code_oaci": "LFLU"},
        {"nom": "Châteauroux-Centre", "code_oaci": "LFLX"},
        {"nom": "Albi-Le Séquestre", "code_oaci": "LFCI"},
        {"nom": "Vannes-Meucon", "code_oaci": "LFRV"},
        {"nom": "Saint-Brieuc Armor", "code_oaci": "LFRT"},
        {"nom": "Aéroport d'Épinal-Mirecourt", "code_oaci": "LFSG"},
        {"nom": "Aurillac-Tronquières", "code_oaci": "LFLW"},
        {"nom": "Bergerac Dordogne Périgord", "code_oaci": "LFBE"},
        {"nom": "Dole-Jura", "code_oaci": "LFGJ"},
        {"nom": "Châlons Vatry", "code_oaci": "LFOK"},
        {"nom": "Carcassonne-Salvaza", "code_oaci": "LFMK"},
        {"nom": "Castres-Mazamet", "code_oaci": "LFCK"},
        {"nom": "Lannion-Côte de Granit", "code_oaci": "LFRO"},
        {"nom": "Rodez-Aveyron", "code_oaci": "LFCR"},
        {"nom": "Perigueux-Bassillac", "code_oaci": "LFBX"},
        {"nom": "Troyes-Barberey", "code_oaci": "LFQB"}
    ]
    for aeroport in aeroports :
        if aeroport ["nom"] == name
            return aeroport["code_oaci"]
    return None 

def exporter_donnees_en_json(data, nom_fichier):
    """
    Exporte les données dans un fichier JSON.

    Args:
        data (dict): Données météorologiques.
        nom_fichier (str): Nom du fichier JSON.
    """
    try:
        with open(nom_fichier, 'w') as fichier:
            json.dump(data, fichier, indent=4)
        print(f"Données exportées dans {nom_fichier}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")
