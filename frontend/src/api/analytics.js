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

export async function listRecentQueries({ limit = 20 }) {
  const response = await fetchWithAuth(
    `${API_BASE}/api/v1/analytics/queries?limit=${limit}`
  );
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}
