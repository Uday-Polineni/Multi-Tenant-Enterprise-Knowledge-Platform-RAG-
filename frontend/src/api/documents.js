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

export async function listDocuments() {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents`);
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function uploadDocument({ file, accessLevel = "public" }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("access_level", accessLevel);

  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function getDocumentStatus({ documentId }) {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents/${documentId}`);
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function updateDocumentAccessLevel({ documentId, accessLevel }) {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents/${documentId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ access_level: accessLevel }),
  });
  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

export async function deleteDocument({ documentId }) {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents/${documentId}`, {
    method: "DELETE",
  });
  if (!response.ok) throw new Error(await parseError(response));
}

export async function openDocumentPdf({ documentId, page }) {
  const response = await fetchWithAuth(`${API_BASE}/api/v1/documents/${documentId}/file`);
  if (!response.ok) throw new Error(await parseError(response));

  const blob = await response.blob();
  const blobUrl = URL.createObjectURL(blob);
  const target = page != null ? `${blobUrl}#page=${page}` : blobUrl;
  window.open(target, "_blank", "noopener,noreferrer");
}
