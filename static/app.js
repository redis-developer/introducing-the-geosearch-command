window.onload = function () {
  const milesToMeters = (miles) => {
    return 1609.344 * miles;
  };

  let userMarker;
  let userShape;

  const myMap = L.map('mapid', {zoomControl: false, doubleClickZoom: false, touchZoom: false, scrollWheelZoom: false, dragging: false}).setView([37.6570598, -122.2636107], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);

  myMap.on('click', (e) => {
    if (userMarker) {
      myMap.removeLayer(userMarker);
    }

    if (userShape) {
      myMap.removeLayer(userShape);
    }
    
    userMarker = L.marker(e.latlng).addTo(myMap);

    const { lat, lng } = e.latlng;

    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
  });

  document.getElementById('searchType').onchange = function (e) {
    const radiusElem = document.getElementById('radius');
    const heightElem = document.getElementById('height');
    const widthElem = document.getElementById('width');

    if (this.value === 'Radius') {
      radiusElem.readOnly = false;
      heightElem.readOnly = true;
      widthElem.readOnly = true;
    } else {
      // Box
      radiusElem.readOnly = true;
      heightElem.readOnly = false;
      widthElem.readOnly = false;
    }
  };

  document.getElementById('searchBtn').onclick = function (e) {
    e.preventDefault();
    const lat = parseFloat(document.getElementById('latitude').value);
    const lng = parseFloat(document.getElementById('longitude').value);
    const radius = parseInt(document.getElementById('radius').value);

    if (lat && lng && radius) {
      // Draw the radius circle on the map...
      const radiusInMeters = milesToMeters(radius);
      userShape = L.circle([lat, lng], {radius: radiusInMeters}).addTo(myMap);
      // TODO call the backend!!
    } else {
      alert('Please complete the form!');
    }
  };
};