import json
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class StepInformation:
    step_keyword: str
    step_name: str
    text: list[str]
    json: list[str]


class StepInformationSaverStrategy(Protocol):
    def save(self, step_information: StepInformation, data: Any) -> StepInformation: ...


class TextStepInformationSaver:
    def save(self, step_information: StepInformation, data: str) -> StepInformation:
        step_information.text.append(data)
        return step_information


class JsonStepInformationSaver:
    def save(self, step_information: StepInformation, data: dict) -> StepInformation:
        step_information.json.append(json.dumps(data, indent=2).strip())
        return step_information


class StepInformationRepo:
    def __init__(self) -> None:
        self.repo: list[StepInformation] = []
        self._savers: dict[str, StepInformationSaverStrategy] = {}

    def add(self, step_keyword: str, step_name: str, information: str | dict) -> None:
        """
        Adds a new step information to the repository.
        """
        step_information = StepInformation(step_keyword, step_name, [], [])
        if self.exists(step_keyword, step_name):
            step_information = self.get(step_keyword, step_name)
            if not step_information:
                return
            self.repo.remove(step_information)

        if not information:
            return
        saver_strategy = self.get_saver(information.__class__.__name__)
        self.repo.append(saver_strategy.save(step_information, information))

    def get(self, step_keyword: str, step_name: str) -> StepInformation | None:
        """
        Returns the saved step information if attached.
        """
        for item in self.repo:
            if item.step_keyword == step_keyword and item.step_name == step_name:
                return item
        return None

    def exists(self, step_keyword: str, step_name: str) -> bool:
        return any(
            item.step_keyword == step_keyword and item.step_name == step_name
            for item in self.repo
        )

    def register_saver(
        self, saver: StepInformationSaverStrategy, for_type: str
    ) -> None:
        self._savers[for_type] = saver

    def get_saver(self, for_type: str) -> StepInformationSaverStrategy:
        saver = self._savers.get(for_type)
        if not saver:
            raise RuntimeWarning(
                f"No information saver strategy register for the image type {for_type}. Try to register a saver with the .register_saver method of this class."
            )
        return saver


step_information_repo = StepInformationRepo()
step_information_repo.register_saver(TextStepInformationSaver(), "str")
step_information_repo.register_saver(JsonStepInformationSaver(), "dict")
