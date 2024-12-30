// Charger les données depuis le fichier JSON
fetch('../Meteo_Aeroport/donnees_meteo.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Injecter les données dans la page HTML
        document.getElementById("airport_name").textContent = data.airport_name || "Non disponible";
        document.getElementById("temperature_max").textContent = data.temperature_max || "Non disponible";
        document.getElementById("temperature_min").textContent = data.temperature_min || "Non disponible";
        document.getElementById("precipitation").textContent = data.precipitation || "Non disponible";
        document.getElementById("vent_vitesse").textContent = data.vent_vitesse || "Non disponible";
        document.getElementById("vent_direction").textContent = data.vent_direction || "Non disponible";
        document.getElementById("ensoleillement").textContent = data.ensoleillement || "Non disponible";
    })
    .catch(error => {
        console.error('Erreur lors du chargement des données :', error);
    });
