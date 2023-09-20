import json
import os
from typing import Protocol


class ILoader(Protocol):
    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[dict]:
        ...


class JsonLoader:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[dict]:
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
