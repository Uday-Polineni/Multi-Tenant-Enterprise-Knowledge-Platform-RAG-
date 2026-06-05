import uuid

from app.core.ai.openai_embedding import get_embedding_provider
from app.core.ai.openai_llm import get_llm_provider
from app.schemas.query import Citation, QueryResponse
from app.services.vector_store import ChunkSearchResult, search

RAG_TOP_K = 5

NO_CONTEXT_ANSWER = (
    "The information is not available in the uploaded documents."
)

RAG_SYSTEM_PROMPT = """You are an enterprise knowledge assistant for a single organization.

Rules:
1. Answer ONLY using the context provided in the user message. Do not use outside knowledge.
2. If the context does not contain enough information to answer, respond exactly with: "The information is not available in the uploaded documents."
3. Be concise, professional, and factual.
4. When you use a fact from the context, reference the source label (e.g. Source 1, Source 2) in your answer.
5. Do not invent policies, numbers, names, or dates that are not in the context."""


def answer_question(
    *,
    organization_id: uuid.UUID,
    question: str,
) -> QueryResponse:
    query_embedding = get_embedding_provider().embed(question)
    hits = search(
        organization_id=organization_id,
        query_embedding=query_embedding,
        top_k=RAG_TOP_K,
    )

    if not hits:
        return QueryResponse(answer=NO_CONTEXT_ANSWER, citations=[])

    system_prompt = _build_system_prompt()
    user_prompt = _build_user_prompt(question=question, hits=hits)
    answer = get_llm_provider().complete(system=system_prompt, user=user_prompt)
    citations = build_citations_from_hits(hits, include=answer.strip() != NO_CONTEXT_ANSWER)

    return QueryResponse(answer=answer, citations=citations)


def _build_system_prompt() -> str:
    return RAG_SYSTEM_PROMPT


def _build_user_prompt(*, question: str, hits: list[ChunkSearchResult]) -> str:
    blocks: list[str] = []
    for index, hit in enumerate(hits, start=1):
        header = f"[Source {index}: {hit.filename}"
        if hit.page_number is not None:
            header += f", page {hit.page_number}"
        if hit.section_name:
            header += f", section {hit.section_name}"
        header += f", chunk_id {hit.chunk_id}"
        header += "]"
        blocks.append(f"{header}\n{hit.content}")

    context = "\n\n".join(blocks)
    return (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above. Reference sources by label (Source 1, Source 2, etc.)."
    )


def build_citations_from_hits(
    hits: list[ChunkSearchResult],
    *,
    include: bool = True,
) -> list[Citation]:
    """Map Chroma hits to API citations (ADR-008), best match first, deduped by chunk_id."""
    if not include:
        return []

    citations: list[Citation] = []
    seen: set[uuid.UUID] = set()

    for hit in hits:
        if hit.chunk_id in seen:
            continue
        seen.add(hit.chunk_id)
        citations.append(search_hit_to_citation(hit))

    return citations


def search_hit_to_citation(hit: ChunkSearchResult) -> Citation:
    section = hit.section_name.strip() if hit.section_name else None
    return Citation(
        document=hit.filename,
        page=hit.page_number,
        section=section or None,
        chunk_id=hit.chunk_id,
    )
