from services.ml_engine.src.rag.vector_store import VectorStore
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(ROOT_DIR))


def test():
    print("Иницилизация ChromaDB")
    store = VectorStore(db_path="./test_chroma_db")

    terra_doc = (
        "Платформа Terra — это интеллектуальная корпоративная система для поиска ответов "
        "по внутренним регламентам, договорам и документам компании. "
        "Система построена на современной микросервисной архитектуре с использованием gRPC и FastAPI. "
        "В качестве локальной нейросети используется модель Qwen 2.5, а в качестве векторного хранилища — ChromaDB. "
        "Главное преимущество Terra — полная конфиденциальность данных, так как обработка происходит локально."
    )

    print("Добавление документа в базу...")
    chunk_count = store.add_document("terra_overview.txt", terra_doc)

    query = "Что такое terra и какие технологии используются в ней?"
    print(f"Ищем в базе ответ на вопрос: {query}")

    results = store.search(query, top_k=2)

    print(f"Найденны ревалетные куски: {len(results)}")
    for i, res in enumerate(results, 1):
        print(f"\n[{i}] Источник: {res['source']}")
        print(f"    Текст: {res['text']}")


if __name__ == "__main__":
    test()
