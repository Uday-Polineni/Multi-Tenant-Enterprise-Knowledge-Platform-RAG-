import re

_ASSISTANT_META_PATTERNS = (
    r"\bwhat can you do\b",
    r"\bwho are you\b",
    r"\bwhat are you\b",
    r"\bwhat do you do\b",
    r"\bhow can you help\b",
    r"\bhow do you work\b",
    r"\byour capabilities\b",
    r"\bwhat is this (?:tool|assistant|bot|chatbot)\b",
)

_SELF_REFERENCE_PATTERNS = (
    r"\btell me about yourself\b",
    r"\babout yourself\b",
)

_ASSISTANT_SUBJECTIVE_PATTERNS = (
    r"\bhow\s+(?:good|bad|well|accurate|reliable|smart|helpful|useful)\s+are\s+you\b",
    r"\bare\s+you\s+(?:good|bad|great|smart|accurate|reliable|helpful|useful)\b",
    r"\brate\s+(?:yourself|you)\b",
    r"\bhow\s+would\s+you\s+rate\s+(?:yourself|you)\b",
)

ASSISTANT_INTRO_ANSWER = """I am your organization's Enterprise Knowledge Assistant.

I answer questions using the documents your team has uploaded — policies, guides, resumes, and other PDFs. I can search across those files, summarize what they say, and cite the source file and page for each fact.

I only use information from your organization's uploaded documents. I do not browse the web or access data outside this workspace.

To get started, ask about a topic covered in your documents, or upload new files from the Documents page."""


def is_assistant_capability_question(question: str) -> bool:
    normalized = question.strip().lower()
    if not normalized:
        return False

    if any(re.search(pattern, normalized) for pattern in _ASSISTANT_META_PATTERNS):
        return True

    return any(re.search(pattern, normalized) for pattern in _SELF_REFERENCE_PATTERNS) and bool(
        re.search(r"\b(you|your)\b", normalized)
    )


def is_assistant_meta_question(question: str) -> bool:
    """True when the user is asking about the assistant itself, not document content."""
    normalized = question.strip().lower()
    if not normalized:
        return False

    if is_assistant_capability_question(question):
        return True

    return any(re.search(pattern, normalized) for pattern in _ASSISTANT_SUBJECTIVE_PATTERNS)


