
# Importation des bibliothèques nécessaires
import requests # type: ignore # Pour faire des requêtes HTTP
from bs4 import BeautifulSoup # type: ignore # Pour analyser le contenu HTML
import re # Pour les expressions régulières
from datetime import datetime # Pour manipuler les dates

def recuperer_donnees_meteobleu(site_aeroport, number):
    # Construction de l'URL avec le code de l'aéroport
    url = f"https://www.meteoblue.com/fr/meteo/semaine/{site_aeroport}?day={number}"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Envoi de la requête HTTP pour récupérer la page
    response = requests.get(url,headers=header)
    # Vérification si la requête a réussi (code 200)
    if response.status_code == 200:
        # Analyse du contenu HTML de la page    
        soup = BeautifulSoup(response.text, 'html.parser')
        # Recherche de la div contenant les informations pour le jour spécifié
        div = soup.find("div", id=f"day{number}")
        
        # Si la div est trouvée
        if div:
            print(div)
            # Extraction des données
            temperature_max = div.find('div', class_='tab-temp-max').get_text(strip=True)
            temperature_min = div.find(class_="tab-temp-min").get_text(strip=True)
            precipitation = div.find(class_="tab-precip").get_text(strip=True)
            vent_vitesse = div.find(class_="wind").get_text(strip=True)
            vent_direction = div.find(class_="wind").find('span')['class'][2]
            ensoleillement = div.find(class_="tab-sun").get_text(strip=True)
           
            # Retourne toutes les données extraites
            return {
                "temperature_max": temperature_max,
                "temperature_min": temperature_min,
                "precipitation": precipitation,
                "vent_vitesse": vent_vitesse,
                "vent_direction": vent_direction,
                "ensoleillement": ensoleillement
            }
    else:
        # Affiche un message d'erreur si la requête échoue
        print("Erreur lors de la récupération des données:", response.status_code)
        return None
def recuperer_donnees_metar(code_aeroport):
     # Construction de l'URL avec le code de l'aéroport
    url = f"https://metar-taf.com/fr/{code_aeroport}"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Envoi de la requête HTTP pour récupérer la page
    response = requests.get(url,headers=header)
    # Vérification si la requête a réussi (code 200)
    print(response)
    if response.status_code == 200:
        # Analyse du contenu HTML de la page    
        soup = BeautifulSoup(response.text, 'html.parser')
        # Recherche de la div contenant les informations pour le jour spécifié
        div = soup.find("div", id="metar")
        aeroport_name=extr(r'<h1 >(.+?)</h1>',div)
        print (aeroport_name)
