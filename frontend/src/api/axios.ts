// Custom instance of axios

import axios from "axios";

// If localhost, use localhost:8000
// Else, use window.location.origin / api
export default axios.create({
  baseURL: window.location.origin.match(
    /(http:\/\/localhost|http:\/\/127\.0\.0\.1)/
  )
    ? "http://127.0.0.1:8000/"
    : window.location.origin + "/api/",
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
  withXSRFToken: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken"
});
