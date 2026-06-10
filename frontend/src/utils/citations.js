// LLM may cite as (Source 1, Source 2) or shorthand (Source 1, 2, 4)
const SOURCE_REF_PATTERN =
  /\s*\(Source\s+\d+(?:\s*,\s*(?:Source\s+)?\d+)*\)/gi;

export function buildSourceMap(citations) {
  const map = new Map();
  for (const citation of citations ?? []) {
    if (citation?.source_index != null) {
      map.set(citation.source_index, citation);
    }
  }
  return map;
}

export function stripSourceRefs(text) {
  return text.replace(SOURCE_REF_PATTERN, "").trim();
}

export function firstSourceIndex(text) {
  const match = text.match(/\(Source\s+(\d+)/i);
  return match ? Number.parseInt(match[1], 10) : null;
}

export function splitAnswerParagraphs(content) {
  if (!content?.trim()) return [];
  return content.split(/\n\n+/).map((part) => part.trim()).filter(Boolean);
}

export function citationLinkLabel(citation) {
  const base = citation.document.replace(/\.pdf$/i, "");
  const maxLen = Math.max(10, Math.floor(base.length / 2));
  const name = base.length > maxLen ? `${base.slice(0, maxLen)}…` : base;
  return citation.page != null ? `${name} · p.${citation.page}` : name;
}

export function citationLinkTitle(citation) {
  const page = citation.page != null ? ` · p.${citation.page}` : "";
  return `${citation.document}${page}`;
}
