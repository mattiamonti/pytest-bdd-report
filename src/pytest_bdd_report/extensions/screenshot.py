from dataclasses import dataclass
from pytest_bdd_report.extensions.encoder import Base64Encoder, ImageEncoder


@dataclass
class Screenshot:
    feature_name: str
    scenario_name: str
    encoded_image: str


class ScreenshotRepo:
    def __init__(self, encoder: ImageEncoder) -> None:
        self.repo: list[Screenshot] = []
        self.encoder: ImageEncoder = encoder

    def add(self, feature_name: str, scenario_name: str, image: bytes):
        """
        Adds a new screenshot to the repository.

        Raises:
            ValueError: If a screenshot for the given feature and scenario already exists in the repository.
        """
        if self.exists(feature_name, scenario_name):
            raise ValueError(
                f"A screenshot for {feature_name} and {scenario_name} already exists in the repository."
            )
        image_base64 = self.encoder.encode(image)
        self.repo.append(Screenshot(feature_name, scenario_name, image_base64))

    def get(self, feature_name: str, scenario_name: str) -> Screenshot | None:
        """
        Returns the saved screenshot
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


# Object to be used in the different parts of code
screenshot_repo = ScreenshotRepo(encoder=Base64Encoder)
