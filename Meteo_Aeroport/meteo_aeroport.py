from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

# Initialisation de l'outil Flask
app = Flask(__name__)

def fetch_weather_data():
    """
    Récupère les données météo depuis la page web spécifiée.

    :return: Un dictionnaire contenant les données météo extraites ou un message d'erreur.
    :rtype: dict
    """
    url = "https://www.meteoblue.com/fr/meteo/semaine/aéroport-de-lyon–saint-exupéry_france_6299401" 
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraction de données
        weather_data = {
            " Aéroport de Paris-Charles de Gaulle": soup.find("h1", class_="Aéroport de Paris-Charles de Gaulle").text,
            "temperature": soup.find("span", class_="temperature").text,
            "conditions": soup.find("div", class_="weather-conditions").text
        }
        return weather_data
    else:
        return {"error": "Impossible de récupérer les données météo."}

@app.route('/')
def home():
    """
    Route principale de l'application Flask.
    
    :return: Une page HTML rendue avec les données météo.
    :rtype: str
    """
    weather_data = fetch_weather_data()
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
