// Custom instance of axios

import axios from "axios";
import type { AxiosRequestConfig } from "axios";

const getBaseURL = () => {
  if (import.meta.env.DEV) {
    return "http://localhost:8000";
  }
  return `${window.location.origin}/api`;
};

export const customAxios = axios.create({
  baseURL: getBaseURL(),
  timeout: 30000,
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
    paramsSerializer: {
      indexes: null
    },
    cancelToken: source.token
  }).then(({ data }) => data);

  // @ts-ignore
  promise.cancel = () => {
    source.cancel("Query was cancelled");
  };

  return promise;
};
