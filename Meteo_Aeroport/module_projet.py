
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
    url = f"https://www.meteobleu.com/fr/meteo/semain/{site_aeroport}?day={number}"
    soup = get_html_page(url)
    if not soup:
        return None

    div = soup.find("div", id=f"day {number}")
    if div:
        temperature_max = div.find(class_="tab-temps-max").get_text(strip=True) if div.find(class_="tab-temps-max") else None
        temperature_min = div.find(class_="tab-temps-min").get_text(strip=True) if div.find(class_="tab-temps-min") else None
        precipitation = div.find(class_="tab-precip").get_text(strip=True) if div.find(class_="tab-precip") else None
        wind_div = div.find(class_="wind")
        vent_vitesse = wind_div.find_all_next('div')[0].get_text(strip=True) if wind_div and wind_div.find_all_next('div') else None
        vent_direction = wind_div.find('span').get_text(strip=True) if wind_div and wind_div.find('span') else None
        ensoleillement = div.find(class_="tab-sun").get_text(strip=True) if div.find(class_="tab-sun") else None

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
