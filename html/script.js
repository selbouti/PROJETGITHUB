// Charger les données depuis le fichier JSON
fetch('donnees_meteo.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const currentPage = window.location.pathname.split('/').pop();
        // Injecter les données dans la page HTML
        if (currentPage === "index.html") {
        console.log(data)
        document.getElementById("airport_name").textContent = data.airport_name || "Non disponible";
        document.getElementById("temperature_max").textContent = data.temperature_max || "Non disponible";
        document.getElementById("temperature_min").textContent = data.temperature_min || "Non disponible";
        document.getElementById("precipitation").textContent = data.precipitation || "Non disponible";
        document.getElementById("ensoleillement").textContent = data.ensoleillement || "Non disponible";
        document.getElementById("temperature").textContent = data.temperature || "Non disponible";
        document.getElementById("visibility").textContent = data.visibility || "Non disponible";
        document.getElementById("wind_speed").textContent = data.wind_speed || "Non disponible";
        document.getElementById("wind_direction").textContent = data.wind_direction || "Non disponible";
        document.getElementById("cloud_altitude").textContent = data.cloud_altitude || "Non disponible";
        document.getElementById("pressure").textContent = data.pressure || "Non disponible";
        document.getElementById("icone").textContent = data.icone || "Non disponible";
        }
         else if (currentPage === "demain.html") {
        console.log(data)
        document.getElementById("airport_name2").textContent = data.airport_name2 || "Non disponible";
        document.getElementById("temperature_max2").textContent = data.temperature_max2 || "Non disponible";
        document.getElementById("temperature_min2").textContent = data.temperature_min2 || "Non disponible";
        document.getElementById("precipitation2").textContent = data.precipitation2 || "Non disponible";
        document.getElementById("ensoleillement2").textContent = data.ensoleillement2 || "Non disponible";
        document.getElementById("temperature2").textContent = data.temperature2 || "Non disponible";
        document.getElementById("visibility2").textContent = data.visibility2 || "Non disponible";
        document.getElementById("wind_speed2").textContent = data.wind_speed2 || "Non disponible";
        document.getElementById("wind_direction2").textContent = data.wind_direction2 || "Non disponible";
        document.getElementById("cloud_altitude2").textContent = data.cloud_altitude2 || "Non disponible";
        document.getElementById("pressure2").textContent = data.pressure2 || "Non disponible";
        document.getElementById("icone2").textContent = data.icone2 || "Non disponible";
        }
        else if (currentPage === "apres.html") {
        console.log(data)
        document.getElementById("airport_name3").textContent = data.airport_name3 || "Non disponible";
        document.getElementById("temperature_max3").textContent = data.temperature_max3 || "Non disponible";
        document.getElementById("temperature_min3").textContent = data.temperature_min3 || "Non disponible";
        document.getElementById("precipitation3").textContent = data.precipitation3 || "Non disponible";
        document.getElementById("ensoleillement3").textContent = data.ensoleillement3 || "Non disponible";
        document.getElementById("temperature3").textContent = data.temperature3 || "Non disponible";
        document.getElementById("visibility3").textContent = data.visibility3 || "Non disponible";
        document.getElementById("wind_speed3").textContent = data.wind_speed3 || "Non disponible";
        document.getElementById("wind_direction3").textContent = data.wind_direction3 || "Non disponible";
        document.getElementById("cloud_altitude3").textContent = data.cloud_altitude3 || "Non disponible";
        document.getElementById("pressure3").textContent = data.pressure3 || "Non disponible";
        document.getElementById("icone3").textContent = data.icone3 || "Non disponible";
        }
        
    })
    
    
