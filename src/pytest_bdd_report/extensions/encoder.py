import base64
from typing import Protocol


class ImageEncoder(Protocol):
    @staticmethod
    def encode(image_bytes: bytes) -> str: ...


class Base64Encoder:
    @staticmethod
    def encode(image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode("utf-8")

    @staticmethod
    def decode(image_base64: str):
        return base64.b64decode(image_base64)
