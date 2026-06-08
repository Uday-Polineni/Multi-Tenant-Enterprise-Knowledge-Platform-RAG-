from functools import lru_cache

from sentence_transformers import CrossEncoder

from app.core.config import get_settings


class BGERerankerProvider:
    def __init__(self, *, model_name: str, cross_encoder: CrossEncoder | None = None) -> None:
        self._model_name = model_name
        self._model = cross_encoder or CrossEncoder(model_name)

    def rerank(self, query: str, passages: list[str]) -> list[int]:
        if not passages:
            return []
        pairs = [[query, passage] for passage in passages]
        scores = self._model.predict(pairs)
        return sorted(range(len(passages)), key=lambda index: scores[index], reverse=True)


@lru_cache
def get_reranker_provider() -> BGERerankerProvider:
    settings = get_settings()
    return BGERerankerProvider(model_name=settings.reranker_model)
