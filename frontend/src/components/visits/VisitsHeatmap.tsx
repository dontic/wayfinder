import { useEffect, useState } from "react";
import { Map } from "react-map-gl/maplibre";
import { DeckGL } from "@deck.gl/react";
import { HeatmapLayer } from "@deck.gl/aggregation-layers";
import type { VisitPlotResponse } from "@/api/django/api.schemas";

interface VisitsHeatmapProps {
  data: VisitPlotResponse | null;
  isLoading?: boolean;
}

interface VisitPoint {
  coordinates: [number, number];
  weight: number;
}

const INITIAL_VIEW_STATE = {
  longitude: -122.4,
  latitude: 37.8,
  zoom: 11,
  pitch: 0,
  bearing: 0
};

// Dark map style for better heatmap visibility
const DARK_MAP_STYLE =
  "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json";

const VisitsHeatmap = ({ data, isLoading }: VisitsHeatmapProps) => {
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);
  const [visitPoints, setVisitPoints] = useState<VisitPoint[]>([]);

  // Transform GeoJSON features to point data for heatmap
  useEffect(() => {
    if (data?.visits?.features) {
      const points: VisitPoint[] = data.visits.features
        .filter(
          (feature: any) =>
            feature.geometry?.type === "Point" &&
            feature.geometry?.coordinates?.length >= 2
        )
        .map((feature: any) => ({
          coordinates: [
            feature.geometry.coordinates[0],
            feature.geometry.coordinates[1]
          ] as [number, number],
          weight: feature.properties.duration_s || 60
        }));

      setVisitPoints(points);
    } else {
      setVisitPoints([]);
    }
  }, [data]);

  // Auto-fit to data bounds when data loads
  useEffect(() => {
    if (visitPoints.length > 0) {
      let minLng = Infinity;
      let maxLng = -Infinity;
      let minLat = Infinity;
      let maxLat = -Infinity;

      visitPoints.forEach((point) => {
        const [lng, lat] = point.coordinates;
        minLng = Math.min(minLng, lng);
        maxLng = Math.max(maxLng, lng);
        minLat = Math.min(minLat, lat);
        maxLat = Math.max(maxLat, lat);
      });

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
  }, [visitPoints]);

  const layers =
    visitPoints.length > 0
      ? [
          new HeatmapLayer({
            id: "visits-heatmap",
            data: visitPoints,
            getPosition: (d: VisitPoint) => d.coordinates,
            getWeight: () => 1,
            radiusPixels: 50,
            intensity: 2,
            threshold: 0.01
          })
        ]
      : [];

  return (
    <div className="relative w-full h-full">
      <DeckGL
        initialViewState={viewState}
        controller={true}
        layers={layers}
        style={{ position: "relative", width: "100%", height: "100%" }}
        onViewStateChange={({ viewState: newViewState }) => {
          if (newViewState && "longitude" in newViewState) {
            setViewState({
              longitude: newViewState.longitude,
              latitude: newViewState.latitude,
              zoom: newViewState.zoom,
              pitch: newViewState.pitch || 0,
              bearing: newViewState.bearing || 0
            });
          }
        }}
      >
        <Map reuseMaps mapStyle={DARK_MAP_STYLE} />
      </DeckGL>

      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-10">
          <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg shadow-lg">
            <div className="flex items-center gap-3">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-400"></div>
              <span className="text-sm font-medium text-zinc-100">
                Loading visits...
              </span>
            </div>
          </div>
        </div>
      )}

      {!isLoading && !data && (
        <div className="absolute inset-0 flex items-center justify-center bg-zinc-900/90 z-10">
          <div className="text-center p-6">
            <p className="text-lg font-medium text-zinc-200">
              No data to display
            </p>
            <p className="text-sm text-zinc-400 mt-2">
              Select a date range and click "Apply Filter"
            </p>
          </div>
        </div>
      )}

      {!isLoading && data && visitPoints.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center bg-zinc-900/90 z-10">
          <div className="text-center p-6">
            <p className="text-lg font-medium text-zinc-200">No visits found</p>
            <p className="text-sm text-zinc-400 mt-2">
              Try selecting a different date range
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default VisitsHeatmap;
