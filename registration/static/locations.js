

//$.getJSON("data.json", async data => {
//instead of local table, get data from python

//})


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

