var map = null;

if (map !== undefined && map !== null) {
    map.remove(); // should remove the map from UI and clean the inner children of DOM element
    console.log(map); // nothing should actually happen to the value of mymap
}

if(sessionStorage.getItem('lat') !== null && sessionStorage.getItem('lon') !== null) {
    lat = sessionStorage.getItem('lat');
    lon = sessionStorage.getItem('lon');
} else {
    lat = 45.166672;
    lon = 5.71667;
}

console.log(lat);
console.log(lon);

map = L.map('map').setView([lat, lon], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function addMarker() {
    L.marker([lat, lon]).addTo(map);
}