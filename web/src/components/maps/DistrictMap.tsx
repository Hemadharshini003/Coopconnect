import React, { useEffect, useRef } from 'react';
import L from 'leaflet';

export const DistrictMap: React.FC = () => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<L.Map | null>(null);

  useEffect(() => {
    if (mapContainer.current && !mapInstance.current) {
      // Center map on Nashik district coordinates
      const map = L.map(mapContainer.current).setView([19.9975, 73.7898], 10);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(map);

      // Cooperative locations in Nashik
      const locations = [
        { lat: 19.8450, lng: 73.9920, title: 'Pragati Dairy Cooperative (Sinnar)', members: '45 Members' },
        { lat: 20.0810, lng: 74.1120, title: 'Sahyadri Farmer Cooperative (Niphad)', members: '120 Members' },
        { lat: 19.9320, lng: 73.8340, title: 'Ujjwal Women Artisan Cooperative (Deolali)', members: '35 Members' },
      ];

      locations.forEach((loc) => {
        L.marker([loc.lat, loc.lng])
          .addTo(map)
          .bindPopup(`<b>${loc.title}</b><br/>${loc.members}`);
      });

      mapInstance.current = map;
    }

    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
        mapInstance.current = null;
      }
    };
  }, []);

  return (
    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-slate-800">Nashik District Cooperative GIS Coverage</h3>
        <span className="text-xs text-slate-500 font-mono">3 Cooperatives Mapped</span>
      </div>
      <div ref={mapContainer} className="h-64 w-full rounded-lg z-10 border border-slate-200" />
    </div>
  );
};
