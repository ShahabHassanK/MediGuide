from langchain_text_splitters import RecursiveCharacterTextSplitter

_medlineplus_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],
)

_medquad_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def chunk_medlineplus(doc: dict) -> list[dict]:
    splits = _medlineplus_splitter.split_text(doc["text"])
    chunks = []
    for i, text in enumerate(splits):
        chunk = {k: v for k, v in doc.items() if k != "text"}
        chunk["text"] = text
        chunk["chunk_index"] = i
        chunk["total_chunks"] = len(splits)
        chunks.append(chunk)
    return chunks


def chunk_medquad(doc: dict) -> list[dict]:
    if len(doc["text"]) <= 1200:
        return [{**doc, "chunk_index": 0, "total_chunks": 1}]
    splits = _medquad_splitter.split_text(doc["text"])
    chunks = []
    for i, text in enumerate(splits):
        chunk = {k: v for k, v in doc.items() if k != "text"}
        chunk["text"] = text
        chunk["chunk_index"] = i
        chunk["total_chunks"] = len(splits)
        chunks.append(chunk)
    return chunks
