// @ts-nocheck
import type {
  VisitPlotlyResponse,
  WayfinderOverlandCreate200,
  WayfinderOverlandCreateBodyOne,
  WayfinderOverlandCreateBodyThree,
  WayfinderOverlandCreateBodyTwo,
  WayfinderTokenRetrieve200,
  WayfinderTokenRetrieveParams,
  WayfinderTripsPlotRetrieveParams,
  WayfinderVisitsPlotRetrieveParams,
} from "../api.schemas";

import { customAxiosInstance } from "../../axios";

type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];

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
 * Endpoint for generating a path plot of trips within a specified date range.
 */
export const wayfinderTripsPlotRetrieve = (
  params: WayfinderTripsPlotRetrieveParams,
  options?: SecondParameter<typeof customAxiosInstance<VisitPlotlyResponse>>,
) => {
  return customAxiosInstance<VisitPlotlyResponse>(
    { url: `/wayfinder/trips/plot/`, method: "GET", params },
    options,
  );
};
/**
 * Endpoint for generating a density map of visits within a specified date range.
 */
export const wayfinderVisitsPlotRetrieve = (
  params: WayfinderVisitsPlotRetrieveParams,
  options?: SecondParameter<typeof customAxiosInstance<VisitPlotlyResponse>>,
) => {
  return customAxiosInstance<VisitPlotlyResponse>(
    { url: `/wayfinder/visits/plot/`, method: "GET", params },
    options,
  );
};
export type WayfinderOverlandCreateResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderOverlandCreate>>
>;
export type WayfinderTokenRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderTokenRetrieve>>
>;
export type WayfinderTripsPlotRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderTripsPlotRetrieve>>
>;
export type WayfinderVisitsPlotRetrieveResult = NonNullable<
  Awaited<ReturnType<typeof wayfinderVisitsPlotRetrieve>>
>;
