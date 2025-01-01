// Charger les données depuis le fichier JSON
fetch('donnees_meteo.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Injecter les données dans la page HTML
        console.log(data)
        document.getElementById("airport_name").textContent = data.airport_name || "Non disponible";
        document.getElementById("temperature_max").textContent = data.temperature_max || "Non disponible";
        document.getElementById("temperature_min").textContent = data.temperature_min || "Non disponible";
        document.getElementById("precipitation").textContent = data.precipitation || "Non disponible";
        document.getElementById("vent_vitesse").textContent = data.vent_vitesse || "Non disponible";
        document.getElementById("vent_direction").textContent = data.vent_direction || "Non disponible";
        document.getElementById("ensoleillement").textContent = data.ensoleillement || "Non disponible";
        document.getElementById("temperature").textContent = data.temperature || "Non disponible";
        document.getElementById("visibility").textContent = data.visibility || "Non disponible";
        document.getElementById("wind_speed").textContent = data.wind_speed || "Non disponible";
        document.getElementById("wind_direction").textContent = data.wind_direction || "Non disponible";
        document.getElementById("cloud_altitude").textContent = data.cloud_altitude || "Non disponible";
        document.getElementById("pressure").textContent = data.pressure || "Non disponible";
        document.getElementById("icone").textContent = data.icone || "Non disponible";
        
    })
    
    .catch(error => {
        console.error('Erreur lors du chargement des données :', error);
    });
