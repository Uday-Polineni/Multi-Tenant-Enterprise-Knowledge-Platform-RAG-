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

export async function askQuestion({ question, accessToken }) {
  const response = await fetch(`${API_BASE}/api/v1/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) throw new Error(await parseError(response));
  return response.json();
}

/**
 * Stream RAG answer via SSE. Events: citations → token* → done | error
 */
export async function askQuestionStream({
  question,
  accessToken,
  onCitations,
  onToken,
  onDone,
}) {
  const response = await fetch(`${API_BASE}/api/v1/query/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) throw new Error(await parseError(response));

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      if (!part.trim()) continue;

      let event = "message";
      let dataLine = "";
      for (const line of part.split("\n")) {
        if (line.startsWith("event: ")) event = line.slice(7).trim();
        if (line.startsWith("data: ")) dataLine = line.slice(6);
      }
      if (!dataLine) continue;

      const payload = JSON.parse(dataLine);
      if (event === "citations") {
        onCitations?.(payload.citations ?? [], payload.stage_timings_ms);
      } else if (event === "token") {
        onToken?.(payload.text ?? "");
      } else if (event === "done") {
        onDone?.(payload);
      } else if (event === "error") {
        throw new Error(payload.detail || "Stream failed");
      }
    }
  }
}
