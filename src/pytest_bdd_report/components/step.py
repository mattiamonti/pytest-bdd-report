from dataclasses import dataclass


@dataclass
class Step:
    keyword: str
    name: str
    line: int
    status: str
    duration: int
    error_message: str = ""
