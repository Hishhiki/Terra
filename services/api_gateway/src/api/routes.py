from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pypdf import PdfReader
import io
import json

from services.api_gateway.src.grpc_client import TerraGrpcClient

router = APIRouter()
grpc_client = TerraGrpcClient()


class ChatQueryRequest(BaseModel):
    query: str


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "api_gateway"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    content_bytes = await file.read()
    text = ""

    if filename.endswith(".txt"):
        text = content_bytes.decode("utf-8", errors="ignore")
    elif filename.endswith(".pdf"):
        pdf_reader = PdfReader(io.BytesIO(content_bytes))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    else:
        raise HTTPException(
            status_code=400, detail="Поддерживаются только форматы .pdf и .txt")

    if not text.strip():
        raise HTTPException(
            status_code=400, detail="Не удалось извлечь текст из файла")

    response = grpc_client.upload_document(filename, text)
    return {
        "success": response.success,
        "chunks_indexed": response.chunks_indexed,
        "message": response.message
    }


@router.post("/chat/stream")
def chat_stream(req: ChatQueryRequest):
    def generate():
        response_stream = grpc_client.stream_chat(req.query)
        for chunk in response_stream:
            data = {
                "token": chunk.token,
                "is_final": chunk.is_final,
                "sources": list(chunk.sources) if chunk.sources else []
            }
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
