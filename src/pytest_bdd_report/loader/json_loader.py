import json
import os
from typing import Any, Protocol


class ILoader(Protocol):
    path: str

    def load(self) -> list[dict[str, Any]]: ...


class JsonLoader:
    def __init__(self, path: str):
        self.path: str = path

    def load(self) -> list[dict[str, Any]]:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
