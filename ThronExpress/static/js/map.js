async function initMap() {
    const response = await fetch('/api/markers');
    const data = await response.json();

    const map = L.map('map').setView([data["center"][0], data["center"][1]], 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const markerIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [15, 25],
        iconAnchor: [12, 25],
        popupAnchor: [1, -34],
        shadowSize: [25, 25]
    });

    let i = 0;
    while(i < data["markers"].length) {
        marker = data["markers"][i];
        var mrk = L.marker([marker[0], marker[1]], {icon: markerIcon}).addTo(map);
        i++;
    }
}

initMap();