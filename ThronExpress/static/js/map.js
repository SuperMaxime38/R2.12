async function initMap() {
    const response = await fetch('/api/markers');
    const data = await response.json();

    const map = L.map('map').setView([data["center"][0], data["center"][1]], 15);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    console.log(data["markers"]);
    console.log(data["markers"][0]);
    let i = 0;
    while(i < data["markers"].length) {
        marker = data["markers"][i];
        console.log("placing marker at " + marker[0] + ", " + marker[1]);
        var marker = L.marker([marker[0], marker[1]]).addTo(map);
        i++;
    }
}

initMap();