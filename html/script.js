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
        document.getElementById("airport_name").textContent = data["aujourd'hui"].airport_name || "Non disponible";
        document.getElementById("temperature_max").textContent = data["aujourd'hui"].temperature_max || "Non disponible";
        document.getElementById("temperature_min").textContent = data["aujourd'hui"].temperature_min || "Non disponible";
        document.getElementById("precipitation").textContent = data["aujourd'hui"].precipitation || "Non disponible";
        document.getElementById("ensoleillement").textContent = data["aujourd'hui"].ensoleillement || "Non disponible";
        document.getElementById("temperature").textContent = data["aujourd'hui"].temperature || "Non disponible";
        document.getElementById("visibility").textContent = data["aujourd'hui"].visibility || "Non disponible";
        document.getElementById("wind_speed").textContent = data["aujourd'hui"].wind_speed || "Non disponible";
        document.getElementById("wind_direction").textContent = data["aujourd'hui"].wind_direction || "Non disponible";
        document.getElementById("cloud_altitude").textContent = data["aujourd'hui"].cloud_altitude || "Non disponible";
        document.getElementById("pressure").textContent = data["aujourd'hui"].pressure || "Non disponible";
        document.getElementById("icone").textContent = data["aujourd'hui"].icone || "Non disponible";
        }
         else if (currentPage === "demain.html") {
        console.log(data)
        document.getElementById("airport_name2").textContent = data["demain"].airport_name || "Non disponible";
        document.getElementById("temperature_max2").textContent = data["demain"].temperature_max || "Non disponible";
        document.getElementById("temperature_min2").textContent = data["demain"].temperature_min || "Non disponible";
        document.getElementById("precipitation2").textContent = data["demain"].precipitation|| "Non disponible";
        document.getElementById("ensoleillement2").textContent = data["demain"].ensoleillement || "Non disponible";
        document.getElementById("temperature2").textContent = data["demain"].temperature || "Non disponible";
        document.getElementById("visibility2").textContent = data["demain"].visibility|| "Non disponible";
        document.getElementById("wind_speed2").textContent = data["demain"].wind_speed || "Non disponible";
        document.getElementById("wind_direction2").textContent = data["demain"].wind_direction || "Non disponible";
        document.getElementById("cloud_altitude2").textContent = data["demain"].cloud_altitude|| "Non disponible";
        document.getElementById("pressure2").textContent = data["demain"].pressure || "Non disponible";
        document.getElementById("icone2").textContent = data["demain"].icone || "Non disponible";
        }
        else if (currentPage === "j2.html") {
        console.log(data)
        document.getElementById("airport_name3").textContent = data["surlendemain"].airport_name|| "Non disponible";
        document.getElementById("temperature_max3").textContent = data["surlendemain"].temperature_max|| "Non disponible";
        document.getElementById("temperature_min3").textContent = data["surlendemain"].temperature_min|| "Non disponible";
        document.getElementById("precipitation3").textContent = data["surlendemain"].precipitation|| "Non disponible";
        document.getElementById("ensoleillement3").textContent = data["surlendemain"].ensoleillement || "Non disponible";
        document.getElementById("temperature3").textContent = data["surlendemain"].temperature|| "Non disponible";
        document.getElementById("visibility3").textContent = data["surlendemain"].visibility || "Non disponible";
        document.getElementById("wind_speed3").textContent = data["surlendemain"].wind_speed|| "Non disponible";
        document.getElementById("wind_direction3").textContent = data["surlendemain"].wind_direction|| "Non disponible";
        document.getElementById("cloud_altitude3").textContent = data["surlendemain"].cloud_altitude || "Non disponible";
        document.getElementById("pressure3").textContent = data["surlendemain"].pressure|| "Non disponible";
        document.getElementById("icone3").textContent = data["surlendemain"].icone|| "Non disponible";
        }
        
    })
    
    
