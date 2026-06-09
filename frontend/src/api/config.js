/** API origin. Empty string = same host (Docker/nginx). Unset = local dev default. */
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL !== undefined
    ? import.meta.env.VITE_API_BASE_URL
    : "http://127.0.0.1:8000";
