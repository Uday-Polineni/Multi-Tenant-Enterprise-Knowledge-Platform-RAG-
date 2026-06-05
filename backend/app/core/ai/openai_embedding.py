from functools import lru_cache

from openai import OpenAI

from app.core.config import get_settings


class OpenAIEmbeddingProvider:
    def __init__(self, *, client: OpenAI | None = None) -> None:
        settings = get_settings()
        self._model = settings.embedding_model
        self._client = client or OpenAI(api_key=settings.openai_api_key)

    def embed(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            model=self._model,
            input=text,
        )
        return list(response.data[0].embedding)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = self._client.embeddings.create(
            model=self._model,
            input=texts,
        )
        ordered = sorted(response.data, key=lambda item: item.index)
        return [list(item.embedding) for item in ordered]


@lru_cache
def get_embedding_provider() -> OpenAIEmbeddingProvider:
    return OpenAIEmbeddingProvider()
