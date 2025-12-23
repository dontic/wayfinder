// @ts-nocheck
export interface ErrorResponse {
  message: string;
}

/**
 * Feature properties (varies by feature type)
 */
export type GeoJSONFeatureProperties = { [key: string]: unknown };

export interface GeoJSONFeature {
  /** Always 'Feature' */
  type?: string;
  geometry: GeoJSONGeometry;
  /** Feature properties (varies by feature type) */
  properties: GeoJSONFeatureProperties;
}

export interface GeoJSONFeatureCollection {
  /** Always 'FeatureCollection' */
  type?: string;
  /** Array of GeoJSON Feature objects */
  features: GeoJSONFeature[];
}

export interface GeoJSONGeometry {
  /** GeoJSON geometry type (e.g., 'Point', 'LineString') */
  type: string;
  /** Coordinates array - format depends on geometry type */
  coordinates: unknown[];
}

export interface Login {
  username?: string;
  email?: string;
  password: string;
}

export interface PasswordChange {
  /** @maxLength 128 */
  new_password1: string;
  /** @maxLength 128 */
  new_password2: string;
}

/**
 * Serializer for requesting a password reset e-mail.
 */
export interface PasswordReset {
  email: string;
}

/**
 * Serializer for confirming a password reset attempt.
 */
export interface PasswordResetConfirm {
  /** @maxLength 128 */
  new_password1: string;
  /** @maxLength 128 */
  new_password2: string;
  uid: string;
  token: string;
}

/**
 * User model w/o password
 */
export interface PatchedUserDetails {
  readonly pk?: number;
  /**
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @maxLength 150
   * @pattern ^[\w.@+-]+$
   */
  username?: string;
  readonly email?: string;
  /** @maxLength 150 */
  first_name?: string;
  /** @maxLength 150 */
  last_name?: string;
}

export interface RestAuthDetail {
  readonly detail: string;
}

export interface TripPlotMeta {
  /** Start datetime of the query range */
  start_datetime: string;
  /** End datetime of the query range */
  end_datetime: string;
  /** Total number of locations in range */
  total_locations: number;
  /** Number of non-stationary locations */
  trip_locations: number;
  /** Number of visits in range */
  visits_count: number;
  /** Number of trip segments */
  trips_count: number;
  /** Whether trips were separated by visits */
  separate_trips: boolean;
  /** Whether visits are included */
  show_visits: boolean;
}

export interface TripPlotResponse {
  /** GeoJSON FeatureCollection containing trip LineString features */
  trips: GeoJSONFeatureCollection;
  /** GeoJSON FeatureCollection containing visit Point features */
  visits: GeoJSONFeatureCollection;
  /** Metadata about the query and results */
  meta: TripPlotMeta;
}

/**
 * User model w/o password
 */
export interface UserDetails {
  readonly pk: number;
  /**
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @maxLength 150
   * @pattern ^[\w.@+-]+$
   */
  username: string;
  readonly email: string;
  /** @maxLength 150 */
  first_name?: string;
  /** @maxLength 150 */
  last_name?: string;
}

export interface VisitPlotlyData {
  coloraxis: string;
  customdata: string[][];
  hovertemplate: string;
  lat: number[];
  lon: number[];
  name: string;
  subplot: string;
  z: number[];
  type: string;
}

export type VisitPlotlyLayoutMapbox = { [key: string]: unknown };

export type VisitPlotlyLayoutColoraxis = { [key: string]: unknown };

export type VisitPlotlyLayoutLegend = { [key: string]: unknown };

export type VisitPlotlyLayoutMargin = { [key: string]: unknown };

export type VisitPlotlyLayoutTemplate = { [key: string]: unknown };

export interface VisitPlotlyLayout {
  mapbox: VisitPlotlyLayoutMapbox;
  coloraxis: VisitPlotlyLayoutColoraxis;
  legend: VisitPlotlyLayoutLegend;
  margin: VisitPlotlyLayoutMargin;
  template: VisitPlotlyLayoutTemplate;
}

export interface VisitPlotlyResponse {
  data: VisitPlotlyData[];
  layout: VisitPlotlyLayout;
}

export type WayfinderOverlandCreateBodyOne = { [key: string]: unknown };

export type WayfinderOverlandCreateBodyTwo = { [key: string]: unknown };

export type WayfinderOverlandCreateBodyThree = { [key: string]: unknown };

export type WayfinderOverlandCreate200 = { [key: string]: unknown };

export type WayfinderOverlandCreate500 = { [key: string]: unknown };

export type WayfinderTokenRetrieveParams = {
  /**
   * Boolean flag to indicate if the token should be regenerated
   */
  recreate?: boolean;
};

export type WayfinderTokenRetrieve200 = {
  token?: string;
};

export type WayfinderTripsPlotRetrieveParams = {
  /**
   * Desired accuracy in meters. 0 means no filtering
   */
  desired_accuracy?: number;
  /**
   * End date for the date range filter (inclusive)
   */
  end_datetime: string;
  /**
   * Flag to indicate if trips should be segmented by visit midtimes
   */
  separate_trips?: boolean;
  /**
   * Flag to indicate if visits should be included in the response
   */
  show_visits?: boolean;
  /**
   * Start date for the date range filter (inclusive)
   */
  start_datetime: string;
};

export type WayfinderVisitsPlotRetrieveParams = {
  /**
   * End date for the date range filter (inclusive)
   */
  end_datetime: string;
  /**
   * Start date for the date range filter (inclusive)
   */
  start_datetime: string;
};
