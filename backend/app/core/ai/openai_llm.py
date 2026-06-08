from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache

from openai import OpenAI

from app.core.config import get_settings


@dataclass
class LLMResult:
    text: str
    token_usage: dict[str, int] | None


class OpenAILLMProvider:
    def __init__(self, *, client: OpenAI | None = None) -> None:
        settings = get_settings()
        self._model = settings.llm_model
        self._client = client or OpenAI(api_key=settings.openai_api_key)

    def complete(self, *, system: str, user: str) -> str:
        return self.complete_with_usage(system=system, user=user).text

    def complete_with_usage(self, *, system: str, user: str) -> LLMResult:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages(system=system, user=user),
        )
        content = response.choices[0].message.content
        text = content.strip() if content else ""
        return LLMResult(text=text, token_usage=self._usage_dict(response.usage))

    def stream_complete_with_usage(
        self, *, system: str, user: str
    ) -> Iterator[str | dict[str, int]]:
        """Yield text tokens, then a final dict with token usage keys."""
        stream = self._client.chat.completions.create(
            model=self._model,
            messages=self._messages(system=system, user=user),
            stream=True,
            stream_options={"include_usage": True},
        )
        token_usage: dict[str, int] | None = None
        for chunk in stream:
            if chunk.usage is not None:
                token_usage = self._usage_dict(chunk.usage)
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
        if token_usage is not None:
            yield token_usage

    @staticmethod
    def _messages(*, system: str, user: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    @staticmethod
    def _usage_dict(usage) -> dict[str, int] | None:
        if usage is None:
            return None
        return {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }


@lru_cache
def get_llm_provider() -> OpenAILLMProvider:
    return OpenAILLMProvider()
