import grpc

from services.ml_engine.src.generated import terra_pb2
from services.ml_engine.src.generated import terra_pb2_grpc


def run_test():
    print("[INFO] Connecting to gRPC server at localhost:50051...")
    channel = grpc.insecure_channel("localhost:50051")
    client = terra_pb2_grpc.TerraServiceStub(channel)

    sample_doc = (
        "Платформа Terra — это интеллектуальная корпоративная система для поиска ответов "
        "по внутренним регламентам, договорам и документам компании. "
        "Система построена на микросервисной архитектуре с использованием gRPC и FastAPI. "
        "В качестве локальной нейросети используется модель Qwen 2.5, а в качестве векторного хранилища — ChromaDB. "
        "Главное преимущество Terra — полная конфиденциальность данных, так как обработка происходит локально."
    )

    print("\n[INFO] Indexing document via gRPC...")
    upload_req = terra_pb2.DocumentUploadRequest(
        filename="terra_architecture.txt",
        content=sample_doc
    )
    upload_res = client.IndexDocument(upload_req)
    print(
        f"[STATUS] Success: {upload_res.success}, Chunks: {upload_res.chunks_indexed}")
    print(f"[MESSAGE] {upload_res.message}")

    query = "Что такое Terra и какие ключевые технологии в ней используются?"
    print(f"\n[QUERY] '{query}'\n")
    print("--- MODEL RESPONSE ---")

    chat_req = terra_pb2.ChatRequest(query=query, chat_history=[])
    response_stream = client.StreamChat(chat_req)

    final_sources = []
    for chunk in response_stream:
        if chunk.token:
            print(chunk.token, end="", flush=True)
        if chunk.is_final and chunk.sources:
            final_sources = list(chunk.sources)

    print("\n----------------------")
    print(f"[SOURCES] {final_sources}")
    print("[INFO] Test completed successfully.")


if __name__ == "__main__":
    run_test()
