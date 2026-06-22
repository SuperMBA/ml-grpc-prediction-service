from __future__ import annotations

import pickle
from pathlib import Path

from server.simple_model import SimpleModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "model.pkl"


def main() -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as f:
        pickle.dump(SimpleModel(), f)
    print(f"Demo model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
