window.onload = function () {
  const milesToMeters = (miles) => {
    return 1609.344 * miles;
  };

  const redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const removeExistingLayers = (includingUserMarker) => {
    if (includingUserMarker && userMarker) {
      myMap.removeLayer(userMarker);
    }

    if (userShape) {
      myMap.removeLayer(userShape);
    }

    currentStations.map((stnMarker) => {
      myMap.removeLayer(stnMarker);
    });
  };

  const addStationMarker = (station) => {
    const stnMarker = L.marker([station.location.latitude, station.location.longitude], { title: station.name }).addTo(myMap);
    currentStations.push(stnMarker);
  };

  let userMarker;
  let userShape;
  let currentStations = [];

  const myMap = L.map('mapid').setView([37.6570598, -122.2636107], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(myMap);

  myMap.on('click', (e) => {
    removeExistingLayers(true);

    userMarker = L.marker(e.latlng, { icon: redIcon }).addTo(myMap);

    const { lat, lng } = e.latlng;

    document.getElementById('latitude').innerHTML = lat;
    document.getElementById('longitude').innerHTML = lng;
  });

  document.getElementById('searchType').onchange = function (e) {
    const radiusElem = document.getElementById('radius');
    const heightElem = document.getElementById('height');
    const widthElem = document.getElementById('width');

    if (this.value === 'Radius') {
      radiusElem.readOnly = false;
      heightElem.readOnly = true;
      widthElem.readOnly = true;
      heightElem.value = '';
      widthElem.value = '';
    } else {
      // Box
      radiusElem.readOnly = true;
      heightElem.readOnly = false;
      widthElem.readOnly = false;
      radiusElem.value = '';
    }
  };

  document.getElementById('dismissError').onclick = function (e) {
    document.getElementById('errorMessage').hidden = true;
  };

  document.getElementById('searchBtn').onclick = async function (e) {
    e.preventDefault();
    removeExistingLayers();

    const errorMessage = document.getElementById('errorMessage');

    errorMessage.hidden = true;

    const lat = parseFloat(document.getElementById('latitude').innerHTML);
    const lng = parseFloat(document.getElementById('longitude').innerHTML);
    const radius = parseInt(document.getElementById('radius').value);

    if (lat && lng && radius) {
      // Draw the radius circle on the map...
      const radiusInMeters = milesToMeters(radius);
      userShape = L.circle([lat, lng], {radius: radiusInMeters}).addTo(myMap);
      
      const response = await fetch(`/api/search/byradius/${lat}/${lng}/${radius}/mi`);
      const stations = await response.json();

      stations.map(addStationMarker);
    } else {
      // Box?
      const height = parseInt(document.getElementById('height').value);
      const width = parseInt(document.getElementById('width').value);
      
      if (lat && lng && height && width) {
        const heightInMeters = milesToMeters(height);
        const widthInMeters = milesToMeters(width);
        const centerLatLng = L.latLng(lat, lng);
        const heightBounds = centerLatLng.toBounds(heightInMeters);
        const widthBounds = centerLatLng.toBounds(widthInMeters);
        const firstNW = heightBounds.getNorthWest();
        const secondNW = widthBounds.getNorthWest();
        const firstSE = heightBounds.getSouthEast();
        const secondSE = widthBounds.getSouthEast();

        const rectNW = L.latLng(firstNW.lat, secondNW.lng);
        const rectSE = L.latLng(firstSE.lat, secondSE.lng);

        userShape = L.rectangle(L.latLngBounds(rectNW, rectSE)).addTo(myMap);

        const response = await fetch(`/api/search/bybox/${lat}/${lng}/${width}/${height}/mi`);
        const stations = await response.json();
        stations.map(addStationMarker);
      } else {
        errorMessage.hidden = false;
      }
    }
  };
};