from services.api_gateway.src.api.routes import router
import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))


app = FastAPI(title="Terra Gateway", version="1.0.0")
app.include_router(router, prefix="/api")

STATIC_DIR = Path(__file__).parent / "src" / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def serve_idx():
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    print("[Gateway] Starting API at http://localhost:8000")
    uvicorn.run("services.api_gateway.main:app",
                host="0.0.0.0", port=8000, reload=True)
