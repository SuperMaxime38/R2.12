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

    let nearestToilet = data["markers"][0];
    let nearestDist = calc_dist(data["center"][0], data["center"][1], nearestToilet[0], nearestToilet[1]);

    while(i < data["markers"].length) {
        marker = data["markers"][i];
        if(data["nearest"] == true) {

            dist = calc_dist(data["center"][0], data["center"][1], marker[0], marker[1]);
            if(nearestDist > dist) {
                nearestDist = dist;
                nearestToilet = marker;
            }

        } else {
            if(
            !(data["hasShower"] && !marker[3]) &&
            !(data["hasDisabledAccess"] && !marker[4]) &&
            !(data["hasChangingRoom"] && !marker[5]) &&
            !(data["hasLuxury"] && !marker[6]) &&
            !(calc_dist(data["center"][0], data["center"][1], marker[0], marker[1]) > data["distance"])
            )
            {
                var mrk = L.marker([marker[0], marker[1]], {icon: markerIcon}).addTo(map);
            }
        }
        i++;
    }

    if(data["nearest"] == true) {
        var mrk = L.marker([nearestToilet[0], nearestToilet[1]], {icon: markerIcon}).addTo(map);
    }
}

async function calc_dist(lat1, lon1, lat2, lon2) {

    const R = 6371e3;
    const phi1 = lat1 * Math.PI/180;
    const phi2 = lat2 * Math.PI/180;

    const deltaPhi = (lat2 - lat1) * Math.PI/180;
    const deltaLambda = (lon2 - lon1) * Math.PI/180;

    const a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) + Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c;

}

initMap();