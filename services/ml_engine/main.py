from services.ml_engine.src.server import serve
import sys
from pathlib import Path
import ollama
import httpx

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))


def check_and_pull_model():
    model_name = "qwen2.5:1.5b"
    print(
        f"[ML Engine] Checking Ollama connection and model '{model_name}'...", flush=True)

    try:
        ollama.list()
    except httpx.ConnectError:
        print("[ERROR] Ollama is not running or not installed.", flush=True)
        print("Please install Ollama from https://ollama.com/ and start the service.", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Connection to Ollama failed: {e}", flush=True)
        sys.exit(1)

    try:
        ollama.show(model_name)
        print(f"[ML Engine] Model '{model_name}' is ready.", flush=True)
    except ollama.ResponseError as e:
        if e.status_code == 404:
            print(
                f"[ML Engine] Model '{model_name}' not found locally.", flush=True)
            print(
                f"[ML Engine] Starting automatic streaming download...\n", flush=True)

            try:
                last_percent = -5
                for progress in ollama.pull(model_name, stream=True):
                    status = progress.get("status", "")

                    if "completed" in progress and "total" in progress:
                        percent = (
                            progress["completed"] / progress["total"]) * 100 if progress["total"] > 0 else 0

                        # Печатаем лог в Docker только каждые 5% прогресса
                        if percent - last_percent >= 5:
                            completed_mb = progress["completed"] / \
                                (1024 * 1024)
                            total_mb = progress["total"] / (1024 * 1024)
                            print(
                                f"[Download] {status}: {completed_mb:.1f} MB / {total_mb:.1f} MB ({percent:.1f}%)", flush=True)
                            last_percent = percent
                    else:
                        print(f"[Download] {status}", flush=True)

                print("\n[ML Engine] Model downloaded successfully!", flush=True)
            except Exception as pull_err:
                print(
                    f"\n[ERROR] Failed during download: {pull_err}", flush=True)
                sys.exit(1)
        else:
            print(f"[ERROR] Failed to check model status: {e}", flush=True)
            sys.exit(1)


if __name__ == "__main__":
    check_and_pull_model()
    serve()
