const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

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

export async function register({ email, password, organizationName }) {
  const response = await fetch(`${API_BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password,
      organization_name: organizationName,
    }),
  });
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
