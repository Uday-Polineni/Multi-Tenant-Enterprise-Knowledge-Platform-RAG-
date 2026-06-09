import { fetchWithAuth } from "./session.js";

import { API_BASE } from "./config.js";

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

export async function register({ email, password, organizationName, inviteToken }) {
  const body = { email, password };
  if (inviteToken) {
    body.invite_token = inviteToken;
  } else {
    body.organization_name = organizationName;
  }

  const response = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function inviteUser({ email, role }) {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/auth/invite`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, role }),
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function fetchDemoCredentials() {
  const response = await fetch(`${API_BASE}/api/v1/auth/demo-credentials`);
  if (response.status === 404) return null;
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function login({ email, password }) {
  const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}
