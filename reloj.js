let isAlarmOn = false;

document.getElementById("alarmButton").addEventListener("click", function() {
    let alarm = document.getElementById("alarmSound");

    if (!isAlarmOn) {
        alarm.play().catch(error => console.error("Error al reproducir el sonido:", error));
        this.textContent = "Detener Alarma";
    } else {
        alarm.pause();
        alarm.currentTime = 0;
        this.textContent = "Activar Alarma";
    }

    isAlarmOn = !isAlarmOn;
});

function simulateCall() {
    document.getElementById("call").style.display = "block";
}

function endCall() {
    document.getElementById("call").style.display = "none";
}

let map;
let marker;

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(function(position) {
            document.getElementById("location").innerText = 
                "Latitud: " + position.coords.latitude + ", Longitud: " + position.coords.longitude;
            updateMap(position.coords.latitude, position.coords.longitude);
        });
    } else {
        document.getElementById("location").innerText = "Geolocalización no soportada";
    }
}

function updateMap(lat, lng) {
    if (!map) {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: lat, lng: lng },
            zoom: 15
        });
        marker = new google.maps.Marker({
            position: { lat: lat, lng: lng },
            map: map
        });
    } else {
        map.setCenter({ lat: lat, lng: lng });
        marker.setPosition({ lat: lat, lng: lng });
    }
}

window.onload = getLocation;
