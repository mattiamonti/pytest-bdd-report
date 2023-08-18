from utils.json_util import save_to_json, load_from_json


class StepDetails:
    """
    Represent the details of a BDD step within a scenario.

    Attributes:
        step_details (dict): A dictionary containing the details of the step.
            - "feature": The feature related to the step.
            - "scenario": The scenario related to the step.
            - "status": The status of the step (e.g., "passed", "failed").
            - "type": The type of step (e.g., "given", "when", "then").
            - "step": The description of the step.
            - "exception": Any exception information related to the step.
            - "nodeid": The unique identifier of the step.
    """

    def __init__(
        self, feature, scenario, status, type, step, exception, nodeid
    ) -> None:
        self.step_details: dict = {
            "feature": feature,
            "scenario": scenario,
            "status": status,
            "type": type,
            "step": step,
            "exception": exception,
            "nodeid": nodeid,
        }

    def append_to_json(self, path: str) -> None:
        """
        Append the step details to a specified JSON file.

        Args:
            path (str): The path to the JSON file.
        """
        results = load_from_json(path)
        # append the step details to the steps information
        results.append(self.step_details)
        save_to_json(results, path)
