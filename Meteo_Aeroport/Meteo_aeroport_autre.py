import requests  # Pour effectuer des requêtes HTTP
from bs4 import BeautifulSoup  # Pour analyser le contenu HTML
import re  # Pour effectuer des recherches dans le texte avec des expressions régulières
from datetime import datetime  # Pour manipuler les dates et heures

def site_allmetsat(airport_name):
    """
    Recherche l'URL Allmetsat d'un aéroport.

    :param airport_name: Nom de l'aéroport à rechercher.
    :return: URL du site Allmetsat pour l'aéroport, ou None en cas d'erreur.
    """
    query = f"{airport_name} site:allmetsat.com"
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', {'class': 'tF2Cxc'}).find('a')['href']
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return None

def site_meteoblue(airport_name):
    """
    Recherche l'URL Meteoblue d'un aéroport.

    :param airport_name: Nom de l'aéroport à rechercher.
    :return: URL du site Meteoblue pour l'aéroport, ou None en cas d'erreur.
    """
    query = f"{airport_name} meteo semaine site:meteoblue.com"
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', {'class': 'tF2Cxc'}).find('a')['href']
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return None

def weathertoday(site_allmetsat1):
    """
    Récupère les données météo actuelles depuis Allmetsat.

    :param site_allmetsat1: URL du site Allmetsat pour l'aéroport.
    :return: Un tuple contenant les données météo (vitesse du vent, direction du vent, température, humidité, pression, visibilité, nuages),
             ou None en cas d'erreur.
    """
