// @ts-nocheck
export interface ErrorResponse {
  message: string;
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
   * Flag to indicate if trips should be colored
   */
  color_trips?: boolean;
  /**
   * Desired accuracy in meters. 0 means no filtering
   */
  desired_accuracy?: number;
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
