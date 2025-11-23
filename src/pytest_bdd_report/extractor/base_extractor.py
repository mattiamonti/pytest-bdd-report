from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar("T")


class BaseExtractor(ABC, Generic[T]):
    def extract_from(self, data: list[dict[str, Any]]) -> list[T]:
        """
        Extract the objects from the raw data passed.
        """
        return [self.create_item(item_data) for item_data in data]

    @abstractmethod
    def create_item(self, data: dict[str, Any]) -> T:
        """
        Create one item from the data passed.
        """
        ...
