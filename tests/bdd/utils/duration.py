from playwright.sync_api import Page, Locator, expect


def get_duration(locator: Locator) -> float:
    test_ids = ["feature-duration", "scenario-duration", "step-duration"]
    for test_id in test_ids:
        element = locator.get_by_test_id(test_id)
        if element.is_visible():
            duration = element.all_inner_texts()
            break
    return _extract_duration_from_string(duration[0])

def _extract_duration_from_string(duration: str) -> float:
    duration = (
        duration.replace("Executed in ", "").replace("ms", "").replace("m", "").replace("s", "")
    )
    return float(duration)