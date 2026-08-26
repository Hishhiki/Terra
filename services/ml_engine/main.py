from services.ml_engine.src.server import serve
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))


if __name__ == "__main__":
    serve()
