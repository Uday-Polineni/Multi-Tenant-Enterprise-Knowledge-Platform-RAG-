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

export async function listDocuments({ accessToken }) {
  const response = await fetch(`${API_BASE}/api/v1/documents`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
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

export async function getDocumentStatus({ documentId, accessToken }) {
  const response = await fetch(`${API_BASE}/api/v1/documents/${documentId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function deleteDocument({ documentId, accessToken }) {
  const response = await fetch(`${API_BASE}/api/v1/documents/${documentId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) throw new Error(await parseError(response));
}

/** Fetch PDF with auth and open in a new tab (optional #page=N). */
export async function openDocumentPdf({ documentId, page, accessToken }) {
  const response = await fetch(`${API_BASE}/api/v1/documents/${documentId}/file`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) throw new Error(await parseError(response));

  const blob = await response.blob();
  const blobUrl = URL.createObjectURL(blob);
  const target = page != null ? `${blobUrl}#page=${page}` : blobUrl;
  window.open(target, "_blank", "noopener,noreferrer");
}
