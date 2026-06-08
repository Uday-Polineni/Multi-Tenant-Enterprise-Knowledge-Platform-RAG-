from tests.regression.corpus_large import LARGE_DOCUMENTS, verify_fact_in_pdf, write_large_corpus
from tests.regression.question_bank_large import build_large_question_bank


def test_ten_large_documents_defined():
    assert len(LARGE_DOCUMENTS) == 10
    for doc in LARGE_DOCUMENTS:
        assert 200 <= doc.page_count <= 300


def test_hundred_questions_generated():
    questions = build_large_question_bank(questions_per_doc=10)
    assert len(questions) == 100


def test_mini_pdf_ground_truth_roundtrip(tmp_path):
    from tests.regression.corpus_large import LargeDocument

    mini = LargeDocument("tst", "mini_test.pdf", "Test", 3)
    path = write_large_corpus(tmp_path, documents=(mini,))[0]
    fact = mini.fact_for_page(2)
    assert verify_fact_in_pdf(path, fact)
