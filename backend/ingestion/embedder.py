from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("NeuML/pubmedbert-base-embeddings")


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = _model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def embed_single(text: str) -> list[float]:
    vector = _model.encode(
        text,
        normalize_embeddings=True,
    )
    return vector.tolist()
