// Load the map only when the coverage section is near the viewport.
(() => {
  const container = document.getElementById('coverage-map');
  if (!container) return;
  const points = [{"slug": "colne", "name": "Colne", "lat": 53.8567728, "lon": -2.1691238}, {"slug": "clitheroe", "name": "Clitheroe", "lat": 53.8717465, "lon": -2.3926783}, {"slug": "whalley", "name": "Whalley", "lat": 53.8215412, "lon": -2.4059596}, {"slug": "barrow", "name": "Barrow", "lat": 53.8406524, "lon": -2.4025937}, {"slug": "burnley", "name": "Burnley", "lat": 53.7907262, "lon": -2.2439196}, {"slug": "silsden", "name": "Silsden", "lat": 53.913185, "lon": -1.9374737}, {"slug": "sutton-in-craven", "name": "Sutton-in-Craven", "lat": 53.8917524, "lon": -1.9922285}, {"slug": "cross-hills", "name": "Cross Hills", "lat": 53.9019787, "lon": -1.9883661}];
  const fallback = container.querySelector('.map-fallback');
  function start() {
    const script = document.createElement('script');
    script.src = '/vendor/leaflet/leaflet.js';
    script.onload = () => {
      if (!window.L) return;
      fallback.hidden = true;
      const map = L.map(container, {scrollWheelZoom:false, zoomControl:true, minZoom:8, maxZoom:16});
      const bounds = L.latLngBounds(points.map(p => [p.lat,p.lon]));
      map.fitBounds(bounds, {padding:[38,42]});
      const layer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom:19,
        attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      layer.on('tileerror', () => { container.classList.add('map-tile-error'); });
      layer.on('load', () => {
        if (container.querySelector('.leaflet-tile-loaded')) container.classList.remove('map-tile-error');
      });
      points.forEach(point => {
        const icon = L.divIcon({className:'service-map-pin', html:'<span aria-hidden="true"></span>', iconSize:[24,30], iconAnchor:[12,30], popupAnchor:[0,-29]});
        const marker = L.marker([point.lat,point.lon], {icon, title:point.name, alt:'Explore services in '+point.name, riseOnHover:true}).addTo(map);
        const popup = document.createElement('div');
        const title = document.createElement('strong'); title.textContent = point.name;
        const link = document.createElement('a'); link.href = '/areas/'+point.slug; link.textContent = 'Explore services here →';
        popup.append(title,link); marker.bindPopup(popup);
      });
      const status = document.createElement('p');
      status.className = 'map-error-note';
      status.textContent = 'Map imagery unavailable. Choose an area using the location buttons.';
      container.appendChild(status);
      // Keep the complete coverage visible when orientation or layout changes.
      let width=container.clientWidth;
      if ('ResizeObserver' in window) new ResizeObserver(() => {
        if (container.clientWidth!==width) { width=container.clientWidth;map.invalidateSize();map.fitBounds(bounds,{padding:[38,42]}); }
      }).observe(container);
    };
    script.onerror = () => { fallback.textContent='Map unavailable. Please choose an area using the location buttons.'; };
    document.head.appendChild(script);
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { observer.disconnect(); start(); }
    }, {rootMargin:'150px'});
    observer.observe(container);
  } else start();
})();
