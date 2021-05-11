window.onload = function () {
  let userMarker;

  const myMap = L.map('mapid', {zoomControl: false, doubleClickZoom: false, touchZoom: false, scrollWheelZoom: false, dragging: false}).setView([37.6570598, -122.2636107], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);

  myMap.on('click', (e) => {
    if (userMarker) {
      myMap.removeLayer(userMarker);
    }
    userMarker = L.marker(e.latlng).addTo(myMap);

    const { lat, lng } = e.latlng;

    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
  });
};