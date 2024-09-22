/**
 * Generated by orval v7.1.1 🍺
 * Do not edit manually.
 * API
 * Description placeholder
 * OpenAPI spec version: 1.0.0
 */
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

export type WayfinderVisitsListParams = {
  end_datetime: string;
  start_datetime: string;
};

export type WayfinderTripsPlotRetrieveParams = {
  /**
   * Flag to indicate if trips should be colored
   */
  color_trips?: boolean;
  /**
   * End date for the date range filter (inclusive)
   */
  end_datetime: string;
  /**
   * Flag to indicate if locations during visits should be removed
   */
  locations_during_visits?: boolean;
  /**
   * Flag to indicate if stationary locations should be shown on the plot
   */
  show_stationary?: boolean;
  /**
   * Flag to indicate if visits should be shown on the plot
   */
  show_visits?: boolean;
  /**
   * Start date for the date range filter (inclusive)
   */
  start_datetime: string;
};

export type WayfinderTokenRetrieve200 = {
  token?: string;
};

export type WayfinderTokenRetrieveParams = {
  /**
   * Boolean flag to indicate if the token should be regenerated
   */
  recreate?: boolean;
};

export type WayfinderOverlandCreate500 = { [key: string]: unknown };

export type WayfinderOverlandCreate200 = { [key: string]: unknown };

export type WayfinderOverlandCreateBodyThree = { [key: string]: unknown };

export type WayfinderOverlandCreateBodyTwo = { [key: string]: unknown };

export type WayfinderOverlandCreateBodyOne = { [key: string]: unknown };

export type WayfinderLocationsListParams = {
  end_datetime: string;
  h_accuracy_lte?: number;
  motion_contains?: string;
  speed_gte?: number;
  start_datetime: string;
};

export interface VisitPlotlyResponse {
  data: VisitPlotlyData[];
  layout: VisitPlotlyLayout;
}

export type VisitPlotlyLayoutTemplate = { [key: string]: unknown };

export type VisitPlotlyLayoutMargin = { [key: string]: unknown };

export type VisitPlotlyLayoutMapbox = { [key: string]: unknown };

export type VisitPlotlyLayoutLegend = { [key: string]: unknown };

export type VisitPlotlyLayoutColoraxis = { [key: string]: unknown };

export interface VisitPlotlyLayout {
  coloraxis: VisitPlotlyLayoutColoraxis;
  legend: VisitPlotlyLayoutLegend;
  mapbox: VisitPlotlyLayoutMapbox;
  margin: VisitPlotlyLayoutMargin;
  template: VisitPlotlyLayoutTemplate;
}

export interface VisitPlotlyData {
  coloraxis: string;
  customdata: string[][];
  hovertemplate: string;
  lat: number[];
  lon: number[];
  name: string;
  subplot: string;
  type: string;
  z: number[];
}

export interface Visit {
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   * @nullable
   */
  altitude?: number | null;
  arrival_date: string;
  /** @pattern ^-?\d{0,1}(?:\.\d{0,2})?$ */
  battery_level: string;
  /** @maxLength 20 */
  battery_state: string;
  departure_date: string;
  /** @maxLength 50 */
  device_id?: string;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  duration: number;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  horizontal_accuracy: number;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,17})?$ */
  latitude: string;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,17})?$ */
  longitude: string;
  time: string;
  /**
   * @maxLength 50
   * @nullable
   */
  unique_id?: string | null;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   * @nullable
   */
  vertical_accuracy?: number | null;
  /** @maxLength 100 */
  wifi?: string;
}

/**
 * User model w/o password
 */
export interface UserDetails {
  readonly email: string;
  /** @maxLength 150 */
  first_name?: string;
  /** @maxLength 150 */
  last_name?: string;
  readonly pk: number;
  /**
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @maxLength 150
   * @pattern ^[\w.@+-]+$
   */
  username: string;
}

export interface RestAuthDetail {
  readonly detail: string;
}

/**
 * User model w/o password
 */
export interface PatchedUserDetails {
  readonly email?: string;
  /** @maxLength 150 */
  first_name?: string;
  /** @maxLength 150 */
  last_name?: string;
  readonly pk?: number;
  /**
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @maxLength 150
   * @pattern ^[\w.@+-]+$
   */
  username?: string;
}

/**
 * Serializer for confirming a password reset attempt.
 */
export interface PasswordResetConfirm {
  /** @maxLength 128 */
  new_password1: string;
  /** @maxLength 128 */
  new_password2: string;
  token: string;
  uid: string;
}

/**
 * Serializer for requesting a password reset e-mail.
 */
export interface PasswordReset {
  email: string;
}

export interface PasswordChange {
  /** @maxLength 128 */
  new_password1: string;
  /** @maxLength 128 */
  new_password2: string;
}

export interface Login {
  email?: string;
  password: string;
  username?: string;
}

export interface Location {
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  altitude: number;
  /** @pattern ^-?\d{0,1}(?:\.\d{0,2})?$ */
  battery_level: string;
  /** @maxLength 20 */
  battery_state: string;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  course: number;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,2})?$ */
  course_accuracy: string;
  /** @maxLength 50 */
  device_id?: string;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  horizontal_accuracy: number;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,17})?$ */
  latitude: string;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,17})?$ */
  longitude: string;
  motion: unknown;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  speed: number;
  /** @pattern ^-?\d{0,3}(?:\.\d{0,2})?$ */
  speed_accuracy: string;
  time: string;
  /**
   * @maxLength 50
   * @nullable
   */
  unique_id?: string | null;
  /**
   * @minimum -2147483648
   * @maximum 2147483647
   */
  vertical_accuracy: number;
  /** @maxLength 100 */
  wifi?: string;
}

export interface ErrorResponse {
  message: string;
}
