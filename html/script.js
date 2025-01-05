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
        document.getElementById("airport_name").textContent = data["metar_taf"]["aujourd'hui"].airport_name || "Non disponible";
        document.getElementById("temperature_max").textContent = data["previsions"]["aujourd'hui"].temperature_max || "Non disponible";
        document.getElementById("temperature_min").textContent = data["previsions"]["aujourd'hui"].temperature_min || "Non disponible";
        document.getElementById("precipitation").textContent = data["previsions"]["aujourd'hui"].precipitation || "Non disponible";
        document.getElementById("ensoleillement").textContent = data["previsions"]["aujourd'hui"].ensoleillement || "Non disponible";
        document.getElementById("temperature").textContent = data["metar_taf"]["aujourd'hui"].temperature || "Non disponible";
        document.getElementById("visibility").textContent = data["metar_taf"]["aujourd'hui"].visibility || "Non disponible";
        document.getElementById("wind_speed").textContent = data["metar_taf"]["aujourd'hui"].wind_speed || "Non disponible";
        document.getElementById("wind_direction").textContent = data["metar_taf"]["aujourd'hui"].wind_direction || "Non disponible";
        document.getElementById("cloud_altitude").textContent = data["metar_taf"]["aujourd'hui"].cloud_altitude || "Non disponible";
        document.getElementById("pressure").textContent = data["metar_taf"]["aujourd'hui"].pressure || "Non disponible";
        document.getElementById("icone").textContent = data["previsions"]["aujourd'hui"].icone || "Non disponible";
        }
         else if (currentPage === "demain.html") {
        console.log(data)
        document.getElementById("airport_name2").textContent = data["metar_taf"]["aujourd'hui"].airport_name || "Non disponible";
        document.getElementById("temperature_max2").textContent = data["previsions"]["demain"].temperature_max || "Non disponible";
        document.getElementById("temperature_min2").textContent = data["previsions"]["demain"].temperature_min || "Non disponible";
        document.getElementById("precipitation2").textContent = data["previsions"]["demain"].precipitation|| "Non disponible";
        document.getElementById("ensoleillement2").textContent = data["previsions"]["demain"].ensoleillement || "Non disponible";
        document.getElementById("icone2").textContent = data["previsions"]["demain"].icone || "Non disponible";
        }
        else if (currentPage === "j2.html") {
        console.log(data)
        document.getElementById("airport_name3").textContent = data["metar_taf"]["aujourd'hui"].airport_name|| "Non disponible";
        document.getElementById("temperature_max3").textContent = data["previsions"]["surlendemain"].temperature_max|| "Non disponible";
        document.getElementById("temperature_min3").textContent = data["previsions"]["surlendemain"].temperature_min|| "Non disponible";
        document.getElementById("precipitation3").textContent = data["previsions"]["surlendemain"].precipitation|| "Non disponible";
        document.getElementById("ensoleillement3").textContent = data["previsions"]["surlendemain"].ensoleillement || "Non disponible";
        document.getElementById("icone3").textContent = data["previsions"]["surlendemain"].icone|| "Non disponible";
        }
        
    })
    
    
