from datasets import load_dataset


def fetch_medquad_docs(max_docs: int = 10000) -> list[dict]:
    print("  Loading MedQuAD dataset from HuggingFace (first run will download ~50 MB)...")
    ds = load_dataset("keivalya/MedQuad-MedicalQnADataset", split="train")

    docs: list[dict] = []
    for record in ds:
        if len(docs) >= max_docs:
            break
        question = (record.get("Question") or "").strip()
        answer = (record.get("Answer") or "").strip()
        if not question or not answer:
            continue
        docs.append(
            {
                "source": "medquad",
                "topic": (record.get("qtype") or "medical_qa").strip(),
                "text": f"Q: {question}\nA: {answer}",
            }
        )

    return docs
