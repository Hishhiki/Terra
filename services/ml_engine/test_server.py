import sys
import grpc

from services.ml_engine.src.generated import terra_pb2
from services.ml_engine.src.generated import terra_pb2_grpc


def run_test():
    print("Connecting...")
    channel = grpc.insecure_channel("localhost:50051")

    client = terra_pb2_grpc.TerraServiceStub(channel)

    request = terra_pb2.ChatRequest(
        query="Привет! Расскажи в трех предложениях, что такое Terra?",
        chat_history=[]
    )

    print("Формируем запрос и ждем стрим ответа")
    response_stream = client.StreamChat(request)

    for chunk in response_stream:
        print(chunk.token, end="", flush=True)

    print("Стрим успешно завершен")


if __name__ == "__main__":
    run_test()
