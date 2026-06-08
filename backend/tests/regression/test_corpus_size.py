from tests.regression.corpus import build_corpus, render_pdf_bytes


def test_corpus_has_fifty_documents():
    docs = build_corpus()
    assert len(docs) == 50
    filenames = {doc.filename for doc in docs}
    assert len(filenames) == 50


def test_each_document_renders_pdf():
    for doc in build_corpus()[:5]:
        data = render_pdf_bytes(doc)
        assert data[:4] == b"%PDF"
