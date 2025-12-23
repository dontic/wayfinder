import { useEffect, useState, useCallback } from "react";
import { Map, useControl } from "react-map-gl/maplibre";
import { MapboxOverlay } from "@deck.gl/mapbox";
import { GeoJsonLayer } from "@deck.gl/layers";
import type { TripPlotResponse } from "@/api/django/api.schemas";

interface TripsMapProps {
  data: TripPlotResponse | null;
  isLoading?: boolean;
}

const INITIAL_VIEW_STATE = {
  longitude: -122.4,
  latitude: 37.8,
  zoom: 11,
  pitch: 0,
  bearing: 0
};

// DeckGL overlay component
function DeckGLOverlay(props: { layers: any[] }) {
  const overlay = useControl(() => new MapboxOverlay({ interleaved: true }));
  overlay.setProps(props);
  return null;
}

const TripsMap = ({ data, isLoading }: TripsMapProps) => {
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);

  // Auto-fit to data bounds when data loads
  useEffect(() => {
    if (data?.trips?.features && data.trips.features.length > 0) {
      let minLng = Infinity;
      let maxLng = -Infinity;
      let minLat = Infinity;
      let maxLat = -Infinity;

      const processFeature = (feature: any) => {
        if (feature.geometry.type === "LineString") {
          feature.geometry.coordinates.forEach((coord: number[]) => {
            minLng = Math.min(minLng, coord[0]);
            maxLng = Math.max(maxLng, coord[0]);
            minLat = Math.min(minLat, coord[1]);
            maxLat = Math.max(maxLat, coord[1]);
          });
        } else if (feature.geometry.type === "Point") {
          const coord = feature.geometry.coordinates;
          minLng = Math.min(minLng, coord[0]);
          maxLng = Math.max(maxLng, coord[0]);
          minLat = Math.min(minLat, coord[1]);
          maxLat = Math.max(maxLat, coord[1]);
        }
      };

      data.trips.features.forEach(processFeature);
      if (data.visits?.features) {
        data.visits.features.forEach(processFeature);
      }
      if (data.stationary?.features) {
        data.stationary.features.forEach(processFeature);
      }

      if (
        isFinite(minLng) &&
        isFinite(maxLng) &&
        isFinite(minLat) &&
        isFinite(maxLat)
      ) {
        const centerLng = (minLng + maxLng) / 2;
        const centerLat = (minLat + maxLat) / 2;

        const lngDiff = maxLng - minLng;
        const latDiff = maxLat - minLat;
        const maxDiff = Math.max(lngDiff, latDiff);

        let zoom = 11;
        if (maxDiff < 0.01) zoom = 14;
        else if (maxDiff < 0.05) zoom = 12;
        else if (maxDiff < 0.1) zoom = 11;
        else if (maxDiff < 0.5) zoom = 9;
        else if (maxDiff < 1) zoom = 8;
        else zoom = 7;

        setViewState({
          longitude: centerLng,
          latitude: centerLat,
          zoom,
          pitch: 0,
          bearing: 0
        });
      }
    }
  }, [data]);

  const layers = [
    data?.trips &&
      new GeoJsonLayer({
        id: "trips-layer",
        data: data.trips as any,
        pickable: true,
        stroked: true,
        filled: false,
        lineWidthScale: 2,
        lineWidthMinPixels: 2,
        getLineColor: [0, 120, 255, 200],
        getLineWidth: 3
      }),
    data?.visits &&
      new GeoJsonLayer({
        id: "visits-layer",
        data: data.visits as any,
        pickable: true,
        stroked: true,
        filled: true,
        pointRadiusMinPixels: 6,
        pointRadiusScale: 1,
        getPointRadius: 8,
        getFillColor: [255, 140, 0, 180],
        getLineColor: [255, 255, 255, 255],
        getLineWidth: 2
      }),
    data?.stationary &&
      new GeoJsonLayer({
        id: "stationary-layer",
        data: data.stationary as any,
        pickable: true,
        stroked: true,
        filled: true,
        pointRadiusMinPixels: 5,
        pointRadiusScale: 1,
        getPointRadius: 6,
        getFillColor: [255, 0, 0, 160],
        getLineColor: [255, 255, 255, 255],
        getLineWidth: 2
      })
  ].filter(Boolean);

  const onMove = useCallback(
    (evt: { viewState: typeof INITIAL_VIEW_STATE }) => {
      setViewState(evt.viewState);
    },
    []
  );

  return (
    <div className="relative w-full h-full">
      <Map
        {...viewState}
        onMove={onMove}
        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        style={{ width: "100%", height: "100%" }}
      >
        <DeckGLOverlay layers={layers} />
      </Map>

      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm z-10">
          <div className="bg-white p-4 rounded-lg shadow-lg">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              <span className="text-sm font-medium">Loading trips...</span>
            </div>
          </div>
        </div>
      )}

      {!isLoading && !data && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/90 z-10">
          <div className="text-center p-6">
            <p className="text-lg font-medium text-gray-700">
              No data to display
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Select a date range and click "Apply Filter"
            </p>
          </div>
        </div>
      )}

      {data && (
        <div className="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-lg text-sm z-10">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-4 h-0.5 bg-[rgb(0,120,255)]"></div>
              <span>Trips: {data.trips?.features?.length || 0}</span>
            </div>
            {data.visits && (
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[rgb(255,140,0)]"></div>
                <span>Visits: {data.visits?.features?.length || 0}</span>
              </div>
            )}
            {data.stationary && (
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-[rgb(255,0,0)]"></div>
                <span>
                  Stationary: {data.stationary?.features?.length || 0}
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TripsMap;
