/** Decode JWT payload for UI only — authorization is enforced by the API. */
export function parseJwtPayload(token) {
  if (!token) return null;
  try {
    const base64Url = token.split(".")[1];
    if (!base64Url) return null;
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const json = atob(base64);
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function getRoleFromToken(token) {
  return parseJwtPayload(token)?.role ?? null;
}

export function getUserIdFromToken(token) {
  return parseJwtPayload(token)?.sub ?? null;
}
