from functools import lru_cache

from openai import OpenAI

from app.core.config import get_settings


class OpenAILLMProvider:
    def __init__(self, *, client: OpenAI | None = None) -> None:
        settings = get_settings()
        self._model = settings.llm_model
        self._client = client or OpenAI(api_key=settings.openai_api_key)

    def complete(self, *, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""


@lru_cache
def get_llm_provider() -> OpenAILLMProvider:
    return OpenAILLMProvider()
