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

export async function uploadDocument({ file, accessToken, accessLevel = "public" }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("access_level", accessLevel);

  const response = await fetch(`${API_BASE}/api/v1/documents/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: formData,
  });

  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}
