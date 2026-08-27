import os
import grpc
from services.api_gateway.src.generated import terra_pb2
from services.api_gateway.src.generated import terra_pb2_grpc


class TerraGrpcClient:
    def __init__(self, target: str = None):
        if target is None:
            target = os.getenv("GRPC_TARGET", "localhost:50051")

        print(f"[Gateway] Connecting to gRPC target: {target}")
        self.channel = grpc.insecure_channel(target)
        self.stub = terra_pb2_grpc.TerraServiceStub(self.channel)

    def upload_document(self, filename: str, content: str):
        request = terra_pb2.DocumentUploadRequest(
            filename=filename,
            content=content
        )
        return self.stub.IndexDocument(request)

    def stream_chat(self, query: str):
        request = terra_pb2.ChatRequest(
            query=query,
            chat_history=[]
        )
        return self.stub.StreamChat(request)
