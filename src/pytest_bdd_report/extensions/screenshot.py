from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from pytest_bdd_report.extensions.encoder import Base64Encoder, ImageEncoder


@dataclass
class Screenshot:
    feature_name: str
    scenario_name: str
    encoded_image: str | None
    path: str | None


class ScreenshotSaverStrategy(Protocol):
    def save(self, feature_name: str, scenario_name: str, image: Any) -> Screenshot: ...


class BytesScreenshotSaver:
    def __init__(self, encoder: ImageEncoder) -> None:
        self.encoder: ImageEncoder = encoder

    def save(self, feature_name: str, scenario_name: str, image: bytes) -> Screenshot:
        return Screenshot(feature_name, scenario_name, self.encoder.encode(image), None)


class PathScreenshotSaver:
    def save(
        self, feature_name: str, scenario_name: str, image: str | Path
    ) -> Screenshot:
        if not isinstance(image, Path):
            image = Path(image)

        if not image.exists():
            raise FileNotFoundError
        return Screenshot(feature_name, scenario_name, None, str(image.absolute()))


class ScreenshotRepo:
    def __init__(self) -> None:
        self.repo: list[Screenshot] = []
        self._savers: dict[str, ScreenshotSaverStrategy] = {}

    def add(self, feature_name: str, scenario_name: str, image: bytes | str | Path):
        """
        Adds a new screenshot to the repository.

        Raises:
            ValueError: If a screenshot for the given feature and scenario already exists in the repository.
        """
        if self.exists(feature_name, scenario_name):
            raise ValueError(
                f"A screenshot for {feature_name} and {scenario_name} already exists in the repository."
            )

        saver_strategy = self.get_saver(image.__class__.__name__)
        self.repo.append(saver_strategy.save(feature_name, scenario_name, image))

    def get(self, feature_name: str, scenario_name: str) -> Screenshot | None:
        """
        Returns the saved screenshot if present.
        """
        for item in self.repo:
            if (
                item.feature_name == feature_name
                and item.scenario_name == scenario_name
            ):
                return item
        return None

    def exists(self, feature_name: str, scenario_name: str) -> bool:
        return any(
            item.feature_name == feature_name and item.scenario_name == scenario_name
            for item in self.repo
        )

    def register_saver(self, saver: ScreenshotSaverStrategy, for_type: str) -> None:
        self._savers[for_type] = saver

    def get_saver(self, for_type: str) -> ScreenshotSaverStrategy:
        saver = self._savers.get(for_type)
        if not saver:
            raise RuntimeWarning(
                f"No screenshot saver strategy register for the image type {for_type}. Try to register a saver with the .register_saver method of this class."
            )
        return saver


# Object to be used in the different parts of code
screenshot_repo = ScreenshotRepo()
screenshot_repo.register_saver(BytesScreenshotSaver(encoder=Base64Encoder), "bytes")
screenshot_repo.register_saver(PathScreenshotSaver(), "str")
screenshot_repo.register_saver(PathScreenshotSaver(), "Path")
screenshot_repo.register_saver(PathScreenshotSaver(), "PosixPath")
