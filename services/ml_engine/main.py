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
        f"[ML Engine] Checking Ollama connection and model '{model_name}'...")

    try:
        ollama.list()
    except httpx.ConnectError:
        print("[ERROR] Ollama is not running or not installed.")
        print("Please install Ollama from https://ollama.com/ and start the service.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Connection to Ollama failed: {e}")
        sys.exit(1)

    try:
        ollama.show(model_name)
        print(f"[ML Engine] Model '{model_name}' is ready.")
    except ollama.ResponseError as e:
        if e.status_code == 404:
            print(f"[ML Engine] Model '{model_name}' not found locally.")
            print(f"[ML Engine] Starting automatic streaming download...\n")

            try:
                current_digest = ""
                for progress in ollama.pull(model_name, stream=True):
                    status = progress.get("status", "")

                    if "completed" in progress and "total" in progress:
                        completed_mb = progress["completed"] / (1024 * 1024)
                        total_mb = progress["total"] / (1024 * 1024)
                        percent = (
                            progress["completed"] / progress["total"]) * 100 if progress["total"] > 0 else 0

                        sys.stdout.write(
                            f"\r[Download] {status}: {completed_mb:.1f} MB / {total_mb:.1f} MB ({percent:.1f}%)   ")
                        sys.stdout.flush()
                    else:
                        print(f"\n[Download] {status}")

                print("\n\n[ML Engine] Model downloaded successfully!")
            except Exception as pull_err:
                print(f"\n[ERROR] Failed during download: {pull_err}")
                sys.exit(1)
        else:
            print(f"[ERROR] Failed to check model status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    check_and_pull_model()
    serve()
