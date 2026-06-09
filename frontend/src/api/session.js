import { parseJwtPayload } from "../utils/jwt.js";

import { API_BASE } from "./config.js";

export const ACCESS_TOKEN_KEY = "eka_access_token";
export const REFRESH_TOKEN_KEY = "eka_refresh_token";
export const EMAIL_KEY = "eka_user_email";

let refreshInFlight = null;
let onTokensUpdated = null;
let onSessionLost = null;

export function setSessionHandlers({ onTokensUpdated: onUpdated, onSessionLost: onLost }) {
  onTokensUpdated = onUpdated ?? null;
  onSessionLost = onLost ?? null;
}

export function saveSession({ accessToken, refreshToken, email }) {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  if (email) localStorage.setItem(EMAIL_KEY, email);
  onTokensUpdated?.({ accessToken, refreshToken });
}

export function clearSession() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(EMAIL_KEY);
  onTokensUpdated?.({ accessToken: "", refreshToken: "" });
}

export function getStoredAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY) || "";
}

export function getStoredRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY) || "";
}

export function isAccessTokenExpired(token) {
  if (!token) return true;
  const payload = parseJwtPayload(token);
  if (!payload?.exp) return true;
  const nowSec = Math.floor(Date.now() / 1000);
  return payload.exp <= nowSec + 30;
}

async function parseError(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
      return data.detail.map((e) => e.msg).join("; ");
    }
    return JSON.stringify(data);
  } catch {
    return response.statusText || "Request failed";
  }
}

export async function refreshSession() {
  if (refreshInFlight) return refreshInFlight;

  const refreshToken = getStoredRefreshToken();
  if (!refreshToken) {
    clearSession();
    onSessionLost?.();
    throw new Error("Session expired");
  }

  refreshInFlight = (async () => {
    const response = await fetch(`${API_BASE}/api/v1/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      clearSession();
      onSessionLost?.();
      throw new Error(await parseError(response));
    }

    const data = await response.json();
    const email = localStorage.getItem(EMAIL_KEY) || "";
    saveSession({
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
      email,
    });
    return data.access_token;
  })();

  try {
    return await refreshInFlight;
  } finally {
    refreshInFlight = null;
  }
}

export async function logoutSession() {
  const refreshToken = getStoredRefreshToken();
  if (refreshToken) {
    try {
      await fetch(`${API_BASE}/api/v1/auth/logout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    } catch {
      // Best-effort server revoke; always clear local session.
    }
  }
  clearSession();
}

export async function fetchWithAuth(url, init = {}) {
  let accessToken = getStoredAccessToken();
  if (!accessToken || isAccessTokenExpired(accessToken)) {
    accessToken = await refreshSession();
  }

  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${accessToken}`);

  let response = await fetch(url, { ...init, headers });

  if (response.status === 401 && getStoredRefreshToken()) {
    accessToken = await refreshSession();
    headers.set("Authorization", `Bearer ${accessToken}`);
    response = await fetch(url, { ...init, headers });
  }

  return response;
}
