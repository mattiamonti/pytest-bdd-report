import json
import os

class JsonLoader:
    def load_json(json_report_path: str) -> list[dict]:
        if os.path.exists(json_report_path):
            with open(json_report_path, "r") as f:
                return json.load(f)
        