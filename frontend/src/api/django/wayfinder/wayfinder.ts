// @ts-nocheck
import type {
  ActivityHistoryResponse,
  PatchedUserSettings,
  TripPlotResponse,
  UserSettings,
  VisitPlotResponse,
  WayfinderOverlandCreate200,
  WayfinderOverlandCreateBodyOne,
  WayfinderOverlandCreateBodyThree,
  WayfinderOverlandCreateBodyTwo,
  WayfinderTokenRetrieve200,
  WayfinderTokenRetrieveParams,
  WayfinderTripsRetrieveParams,
  WayfinderVisitsRetrieveParams,
} from "../api.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

/**
 * Returns pre-computed daily location and visit counts for the past 365 days, grouped by the authenticated user's home timezone.  Data is refreshed nightly at 04:00 UTC by a background task.
 */
export const wayfinderActivityHistoryRetrieve = (
  options?: SecondParameter<
    typeof customAxiosInstance<ActivityHistoryResponse>
  >,
) => {
  return customAxiosInstance<ActivityHistoryResponse>(
    { url: `/wayfinder/activity/history/`, method: "GET" },
    options,
  );
};
/**
 * Endpoint for receiving and storing location and visit data from Overland app.
 */
export const wayfinderOverlandCreate = (
  wayfinderOverlandCreateBody:
    | WayfinderOverlandCreateBodyOne
    | WayfinderOverlandCreateBodyTwo
    | WayfinderOverlandCreateBodyThree,
  options?: SecondParameter<
    typeof customAxiosInstance<WayfinderOverlandCreate200>
  >,
) => {
  return customAxiosInstance<WayfinderOverlandCreate200>(
    {
      url: `/wayfinder/overland/`,
      method: "POST",
      data: wayfinderOverlandCreateBody,
    },
    options,
  );
};
/**
 * Retrieve the current user's settings.
 */
export const wayfinderSettingsRetrieve = (
  options?: SecondParameter<typeof customAxiosInstance<UserSettings>>,
) => {
  return customAxiosInstance<UserSettings>(
    { url: `/wayfinder/settings/`, method: "GET" },
    options,
  );
};
/**
 * Update the current user's settings (e.g. home timezone).
 */
export const wayfinderSettingsPartialUpdate = (
  patchedUserSettings: PatchedUserSettings,
  options?: SecondParameter<typeof customAxiosInstance<UserSettings>>,
) => {
  return customAxiosInstance<UserSettings>(
    {
      url: `/wayfinder/settings/`,
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      data: patchedUserSettings,
    },
    options,
  );
};
/**
 * This endpoint gets or creates a new token for the authenticated user or regenerates an existing one if requested.
 * @summary Get or regenerate authentication token
 */
export const wayfinderTokenRetrieve = (
  params?: WayfinderTokenRetrieveParams,
  options?: SecondParameter<
    typeof customAxiosInstance<WayfinderTokenRetrieve200>
  >,
) => {
  return customAxiosInstance<WayfinderTokenRetrieve200>(
    { url: `/wayfinder/token/`, method: "GET", params },
    options,
  );
};
/**
 * Endpoint for retrieving trip data as GeoJSON within a specified date range. Supports pagination for large datasets.
 */
export const wayfinderTripsRetrieve = (
  params: WayfinderTripsRetrieveParams,
  options?: SecondParameter<typeof customAxiosInstance<TripPlotResponse>>,
) => {
  return customAxiosInstance<TripPlotResponse>(
    { url: `/wayfinder/trips/`, method: "GET", params },
    options,
  );
};
/**
 * Endpoint for retrieving visit data as GeoJSON within a specified date range.
 */
export const wayfinderVisitsRetrieve = (
  params: WayfinderVisitsRetrieveParams,
  options?: SecondParameter<typeof customAxiosInstance<VisitPlotResponse>>,
) => {
  return customAxiosInstance<VisitPlotResponse>(
    { url: `/wayfinder/visits/`, method: "GET", params },
    options,
  );
};
export type WayfinderActivityHistoryRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderActivityHistoryRetrieve>>
>;
export type WayfinderOverlandCreateResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderOverlandCreate>>
>;
export type WayfinderSettingsRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderSettingsRetrieve>>
>;
export type WayfinderSettingsPartialUpdateResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderSettingsPartialUpdate>>
>;
export type WayfinderTokenRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderTokenRetrieve>>
>;
export type WayfinderTripsRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderTripsRetrieve>>
>;
export type WayfinderVisitsRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderVisitsRetrieve>>
>;
