"""100 questions with ground-truth facts from large PDF corpus."""

from __future__ import annotations

from dataclasses import dataclass

from tests.regression.corpus_large import LARGE_DOCUMENTS, PageFact, sample_question_pages


@dataclass(frozen=True)
class LargeRegressionQuestion:
    id: str
    question: str
    ground_truth: PageFact
    expect_any: tuple[str, ...]
    source_file: str
    source_page: int

    @property
    def canonical_answer_hint(self) -> str:
        return (
            f"Page {self.source_page} of {self.source_file} records "
            f"{self.ground_truth.cert_id} with score {self.ground_truth.score}."
        )


def build_large_question_bank(*, questions_per_doc: int = 10) -> list[LargeRegressionQuestion]:
    questions: list[LargeRegressionQuestion] = []
    for document in LARGE_DOCUMENTS:
        pages = sample_question_pages(document.page_count, questions_per_doc)
        for page in pages:
            fact = document.fact_for_page(page)
            qid = f"{document.slug}_p{page:04d}"
            questions.append(
                LargeRegressionQuestion(
                    id=qid,
                    question=(
                        f"According to {document.filename}, what is the certification score "
                        f"for {fact.cert_id} on page {page}?"
                    ),
                    ground_truth=fact,
                    expect_any=(str(fact.score), fact.cert_id),
                    source_file=document.filename,
                    source_page=page,
                )
            )
    return questions


LARGE_RAG_QUESTIONS = build_large_question_bank(questions_per_doc=10)
