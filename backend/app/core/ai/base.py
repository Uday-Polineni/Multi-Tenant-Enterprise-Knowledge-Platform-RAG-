from typing import Protocol


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]:
        """Return a single embedding vector for one text."""

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text, in order."""


class LLMProvider(Protocol):
    def complete(self, *, system: str, user: str) -> str:
        """Return the model's text response for a system + user prompt."""


class RerankerProvider(Protocol):
    def rerank(self, query: str, passages: list[str]) -> list[int]:
        """Return passage indices sorted by relevance to the query (best first)."""
