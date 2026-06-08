from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    upload_dir: str = "data/uploads"

    # Day 3 — AI + vector store
    openai_api_key: str
    chroma_persist_dir: str = "data/chroma"
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"

    # Day 4 — registration + invites
    allow_public_registration: bool = True
    invite_expire_days: int = 7

    # Day 5 — retrieval + reranker
    rag_search_top_k: int = 30
    rag_rerank_top_n: int = 20
    reranker_enabled: bool = False
    reranker_model: str = "BAAI/bge-reranker-base"

    # Ingest — chunk size balances retrieval focus vs LLM context (re-upload after change)
    ingest_chunk_max_chars: int = 1000
    ingest_chunk_overlap_chars: int = 100

    # LLM context — defaults match ingest size = no truncation
    rag_llm_context_chunks: int = 20
    rag_chunk_max_chars: int = 1000

    # Day 6 — Redis cache, rate limit, async embed
    redis_url: str = "redis://127.0.0.1:6379/0"
    cache_ttl_seconds: int = 3600
    rate_limit_per_hour: int = 100
    embed_async: bool = True

    # Phase B1 — semantic answer cache + org version invalidation
    semantic_cache_enabled: bool = True
    semantic_cache_similarity_threshold: float = 0.92
    semantic_cache_max_entries: int = 200

    # Phase B2 — Postgres FTS + Chroma hybrid (RRF merge)
    hybrid_search_enabled: bool = True
    hybrid_rrf_k: int = 60

    # Prototype — upload caps (set to 0 to disable a limit, e.g. in regression tests)
    prototype_max_pdf_pages: int = 15
    prototype_max_documents_per_org: int = 15


@lru_cache
def get_settings() -> Settings:
    return Settings()
