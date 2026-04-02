import json
from dataclasses import dataclass


@dataclass
class StepInformation:
    step_keyword: str
    step_name: str
    text: list[str]
    json: list[str]


class StepInformationRepo:
    def __init__(self) -> None:
        self.repo: list[StepInformation] = []

    def add(self, step_keyword: str, step_name: str, information: str | dict) -> None:
        """
        Adds a new step information to the repository.

        Raises:
            ValueError: If the steps has already information attached.
        """
        step_information = StepInformation(step_keyword, step_name, [], [])
        if self.exists(step_keyword, step_name):
            step_information = self.get(step_keyword, step_name)
        # TODO refactor della logica usando un saver strategy?
        if isinstance(information, str):
            step_information.text.append(information)
        if isinstance(information, dict):
            step_information.json.append(json.dumps(information, indent=2).strip())

        self.repo.append(step_information)

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


step_information_repo = StepInformationRepo()
