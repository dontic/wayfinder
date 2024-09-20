// Custom instance of axios

import axios, { AxiosRequestConfig } from "axios";

export const customAxios = axios.create({
  // Match the origin of the window to determine if we are in development or production
  baseURL: window.location.origin.match(
    /(http:\/\/localhost|http:\/\/127\.0\.0\.1)/
  )
    ? "http://localhost:8000"
    : "/api",
  timeout: import.meta.env.VITE_API_TIMEOUT
    ? import.meta.env.VITE_API_TIMEOUT
    : 10000,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
  withXSRFToken: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken"
});

export const customAxiosInstance = <T>(
  config: AxiosRequestConfig,
  options?: AxiosRequestConfig
): Promise<T> => {
  const source = axios.CancelToken.source();
  const promise = customAxios({
    ...config,
    ...options,
    cancelToken: source.token
  }).then(({ data }) => data);

  // @ts-ignore
  promise.cancel = () => {
    source.cancel("Query was cancelled");
  };

  return promise;
};
