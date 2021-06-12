var map = L.map('map').setView({lat: 49.43, lon: 8.6759873}, 12);
// add the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
}).addTo(map);

// show the scale bar on the lower left corner
L.control.scale().addTo(map);

var yellowIcon = L.icon({
    iconUrl: 'map/marker.svg',
//    shadowUrl: 'map/leaf-shadow.png',

    iconSize:     [38, 95], // size of the icon
    shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});



$.getJSON("map/data.json", async data => {
    for (key in data) {
        value = data[key];
        await $.get(location.protocol + '//nominatim.openstreetmap.org/search?format=json&q='+ value.address, function(data){
            console.log(data);
            lon = data[0].lon;
            lat = data[0].lat;
            var popupStr = '<strong>' + value.name + '</strong><br>' +  value.address + '<br><br>' + '<a href="#">Anmeldung</a>'
            L.marker([lat, lon], {icon: yellowIcon}).addTo(map).bindPopup(popupStr);
        });
    }
})


/* Open when someone clicks on the span element */
function openMap() {
    document.getElementById("mapOverlay").style.display = "block";
    document.body.style.overflow = "hidden";
    map.invalidateSize();
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeMap() {
    document.getElementById("mapOverlay").style.display = "none";
    document.body.style.overflow = "auto";
}

// show a marker on the map
//L.marker({lat: 49.40824, lon: 8.6714711}).bindPopup('Calvary Chapel').addTo(map);

