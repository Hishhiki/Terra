import grpc
from concurrent import futures
import ollama

from services.ml_engine.src.generated import terra_pb2
from services.ml_engine.src.generated import terra_pb2_grpc
from services.ml_engine.src.rag.vector_store import VectorStore


class TerraService(terra_pb2_grpc.TerraServiceServicer):
    def __init__(self):
        print("[ML] Initializing ChromaDB vector store...")
        self.vector_store = VectorStore(db_path="./chroma_db")

    def IndexDocument(self, request, context):
        print(
            f"[gRPC] Indexing document: {request.filename} ({len(request.content)} chars)")
        try:
            chunks_count = self.vector_store.add_document(
                request.filename, request.content)
            return terra_pb2.DocumentUploadResponse(
                success=True,
                chunks_indexed=chunks_count,
                message=f"File '{request.filename}' indexed successfully ({chunks_count} chunks)"
            )
        except Exception as e:
            print(f"[gRPC] Indexing error: {e}")
            return terra_pb2.DocumentUploadResponse(
                success=False,
                chunks_indexed=0,
                message=f"Indexing failed: {e}"
            )

    def StreamChat(self, request, context):
        user_query = request.query
        print(f"[gRPC] User query: {user_query}")

        try:
            search_results = self.vector_store.search(user_query, top_k=3)
            sources = list({res["source"] for res in search_results})

            context_text = "\n\n".join([
                f"--- Source: {res['source']} ---\n{res['text']}"
                for res in search_results
            ])

            if context_text:
                system_prompt = (
                    "Ты — умный корпоративный AI-ассистент платформы Terra.\n"
                    "Отвечай на вопрос пользователя строго на основе предоставленного ниже контекста из документов компании.\n"
                    "Если в контексте нет информации, вежливо скажи, что в базе знаний нет данных по этому вопросу.\n\n"
                    f"=== КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ ===\n{context_text}\n================================"
                )
            else:
                system_prompt = "Ты — умный AI-ассистент платформы Terra. Отвечай кратко и профессионально."

            response_stream = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                stream=True,
                options={"temperature": 0.1}
            )

            for chunk in response_stream:
                token_text = chunk["message"]["content"]
                yield terra_pb2.ChatChunkResponse(
                    token=token_text,
                    is_final=False,
                    sources=[]
                )

            yield terra_pb2.ChatChunkResponse(
                token="",
                is_final=True,
                sources=sources
            )
            print(f"[gRPC] Stream finished. Sources used: {sources}")

        except Exception as e:
            print(f"[gRPC] Generation error: {e}")
            yield terra_pb2.ChatChunkResponse(
                token=f"Server error: {e}",
                is_final=True,
                sources=[]
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    terra_pb2_grpc.add_TerraServiceServicer_to_server(TerraService(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("[ML Engine] gRPC Server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
