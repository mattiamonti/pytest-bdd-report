class ScenarioAggregator:
    """
    Aggregate BDD steps into their corresponding scenarios.

    This class provides methods to aggregate steps information and organize them into
    a dictionary where each scenario includes its related steps.
    """

    def __init__(self) -> None:
        pass

    def aggregate_steps_into_scenario(self, steps_information: list) -> dict:
        """
        Aggregate steps information by scenario.

        Args:
            steps_information (list): A list of step information dictionaries.

        Returns:
            dict: A dictionary where each scenario includes its related steps.
        """
        aggregated_results = {}
        for step in steps_information:
            feature = step["feature"]
            scenario = step["scenario"]
            scenario_key = f"{feature} - {scenario}"

            # Check if the scenario key is already present in aggregated_results
            if scenario_key not in aggregated_results:
                # Initialize a new scenario entry if not present
                aggregated_results[scenario_key] = {
                    "feature": feature,
                    "scenario": scenario,
                    "steps": [self._get_step_information(step)],
                }
            else:
                # Append step information to the existing scenario entry
                aggregated_results[scenario_key]["steps"].append(
                    self._get_step_information(step)
                )
        return aggregated_results

    def _get_step_information(self, step) -> dict:
        """
        Create a dictionary from the step information.

        Args:
            step (dict): The step information dictionary.

        Returns:
            dict: A dictionary containing relevant step details.
        """
        return {
            "type": step["type"],
            "step": step["step"],
            "status": step["status"],
            "nodeid": step["nodeid"],
            "exception": step["exception"],
        }
