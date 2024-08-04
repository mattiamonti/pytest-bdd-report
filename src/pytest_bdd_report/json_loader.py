import json
import os

from pytest_bdd_report.interfaces import ILoader


class JsonLoader(ILoader):
    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[dict]:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
