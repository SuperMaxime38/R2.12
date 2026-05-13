async function initMap() {
    const response = await fetch('/api/markers');
    const data = await response.json();

    const map = L.map('map').setView([data["center"][0], data["center"][1]], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    for(marker in data["markers"]) {
        var marker = L.marker([marker[4], marker[5]]).addTo(map);
    }
}

initMap();