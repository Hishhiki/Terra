import grpc
from concurrent import futures
import ollama

from services.ml_engine.src.generated import terra_pb2
from services.ml_engine.src.generated import terra_pb2_grpc


class TerraService(terra_pb2_grpc.TerraServiceServicer):
    def StreamChat(self, request, context):
        user_query = request.query
        try:
            response_stream = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[
                    {"role": "system",
                        "content": "Ты — умный AI-ассистент платформы Terra."},
                    {"role": "user", "content": user_query}
                ],
                stream=True
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
                sources=[]
            )

        except Exception as e:
            print(f"Error by generation : {e}")

            yield terra_pb2.ChatChunkResponse(
                token=f"Ошибка сервера: {e}",
                is_final=True,
                sources=[]
            )

    def IndexDocument(self, request, context):
        print(
            f"Получен документ: {request.filename}, ({len(request.content)}) символов")

        return terra_pb2.DocumentUploadResponse(
            success=True,
            chunks_indexed=1,
            message=f"Документ '{request.filename}' принят в обработку"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    terra_pb2_grpc.add_TerraServiceServicer_to_server(TerraService(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
