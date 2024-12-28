
import requests  # type: ignore # Pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # type: ignore # Pour analyser le contenu HTML
import re  # Pour les expressions régulières
from datetime import datetime  # Pour manipuler les dates

def get_html_page(url):
    """
    Récupère le contenu HTML d'une page web à partir de son URL.

    Args:
        url (str): L'URL de la page web.

    Returns:
        BeautifulSoup: Objet BeautifulSoup contenant le contenu HTML.
    """
    try:
        response = requests.get(url)
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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page_html = requests.get(url, headers=headers)

    if page_html.status_code==200:
        soup = BeautifulSoup(page_html.text, 'html.parser')
        section = page_html.text
        

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
            "temperature_max": temperature_max,
            "temperature_min": temperature_min,
            "precipitation": precipitation,
            "vent_vitesse": vent_vitesse,
            "vent_direction": vent_direction,
            "ensoleillement": ensoleillement
        }
    else:
        print(f"Div avec id=day {number} introuvable.")
        return None

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
    if not soup:
        return None

    data = {}
    metar_div = soup.find('div', id='metar')
    if metar_div:
        # Nom de l'aéroport
        airport_name_match = re.search(r'<h1 class="h4 mb-0 test-ellipsis">(.+?)</h1>', str(metar_div))
        data['airport_name'] = airport_name_match.group(1).strip() if airport_name_match else None

        # Température
        temp_match = re.search(r'(\d+ \u00b0C)', str(metar_div))
        data['temperature'] = temp_match.group(1).strip() if temp_match else None

        # Visibilité
        visibility_match = re.search(r'<h3 class="mb-0">(\d+ km)</h3>', str(metar_div))
        data['visibility'] = visibility_match.group(1).strip() if visibility_match else None

        # Vitesse et direction du vent
        wind_speed_match = re.search(r'<h3 class="mb-0">(\d+ kt)</h3>', str(metar_div))
        wind_dir_match = re.search(r'(\d{3}\u00b0)', str(metar_div))
        data['wind_speed'] = wind_speed_match.group(1).strip() if wind_speed_match else None
        data['wind_direction'] = wind_dir_match.group(1).strip() if wind_dir_match else None

        # Altitude des nuages
        cloud_alt_match = re.search(r'<h3 class="mb-0">(\d+ ft)</h3>', str(metar_div))
        data['cloud_altitude'] = cloud_alt_match.group(1).strip() if cloud_alt_match else None

        # Pression atmosphérique
        pressure_match = re.search(r'<h3 class="mb-0">(\d+ hPa)</h3>', str(metar_div))
        data['pressure'] = pressure_match.group(1).strip() if pressure_match else None

    return data
