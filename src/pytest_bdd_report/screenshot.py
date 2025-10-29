from typing import Optional, Type

class ScreenshotEmbedder:
    def __init__(self):
        pass

    def _scenario_has_screenshot(feature_id, scenario_id):
        #TODO controlla che uno scenario FALLITO abbia uno screenshot cercando scenario id e feature id nel json "screenshots"
        pass

    def _get_screenshot(feature_id, scenario_id):
        #TODO recupera lo screenshot base64 dato i parametri dal json "screenshots"
        pass

    def create_embed(feature_id, scenario_id):
        #TODO crea l'elemento html con <img....o boh con iniettata l'immagine image_base64
        # questo dovrà poi essere passato all'oggetto ScenarioTemplate in modo da iniettarlo nello scenario
        pass

class ScreenshotRepo:
    def __init__(self) -> None:
        self.repo = []
    
    def add(self, feature_name:str, scenario_name: str, image_base64: str):
        data = {
                "feature_name": feature_name,
                "scenario_name": scenario_name,
                "image_base64": image_base64
            }
        self.repo.append(data)

    def get(self, feature_name: str, scenario_name: str) -> str:
        """
        @return the screenshot image encoded in base64
        """
        for item in self.repo:
            if item["feature_name"] == feature_name and item["scenario_name"] == scenario_name:
                return item["image_base64"]
        return None

# Object to be used in the different parts of code
screenshot_repo = ScreenshotRepo()