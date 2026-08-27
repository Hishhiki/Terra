from pathlib import Path
import chromadb


class VectorStore:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="terra_docs")

    def _chunk_text(self, text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        for word in words:
            word_len = len(word) + 1

            if current_length + word_len > chunk_size and current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append(chunk_str)

                overlap_words = []
                overlap_len = 0
                for w in reversed(current_chunk):
                    if overlap_len + len(w) + 1 <= overlap:
                        overlap_words.insert(0, w)
                        overlap_len += len(w) + 1
                    else:
                        break

                current_chunk = overlap_words
                current_length = overlap_len
            current_chunk.append(word)
            current_length += word_len
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def add_document(self, filename: str, content: str) -> int:
        chunks = self._chunk_text(content)
        if not chunks:
            return 0

        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]

        metadatas = [{"source": filename, "chunk_id": i}
                     for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(
            f"В векторную базу добавлено {len(chunks)} чанков из файла: {filename}")
        return len(chunks)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        matched_chunks = []
        for doc_text, meta in zip(results["documents"][0], results["metadatas"][0]):
            matched_chunks.append({
                "text": doc_text,
                "source": meta.get("source", "Неизвестный источник")
            })

        return matched_chunks
