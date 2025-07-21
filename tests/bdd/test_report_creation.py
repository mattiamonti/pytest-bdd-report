import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path
from playwright.sync_api import Page
import os
from datetime import datetime
from tests.bdd.generator.bdd_generator import (
    BDDTestBuilder,
    BDDFeature,
    BDDScenario,
    create_passed_step,
    create_failed_step,
    create_skipped_step,
)

from tests.bdd.steps.generation_steps import *

scenarios("features/report_creation.feature")