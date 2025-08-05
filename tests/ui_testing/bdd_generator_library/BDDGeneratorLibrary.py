from bdd_generator import (
    BDDTestBuilder,
    BDDFeature,
    BDDScenario,
    create_passed_step,
    create_failed_step,
    create_skipped_step,
)

# Variabili globali per tenere traccia dello stato corrente
_builder = None
_current_feature = None
_current_scenario = None


def create_builder(output_dir):
    """Inizializza il builder con la directory di output"""
    global _builder
    _builder = BDDTestBuilder(output_dir)


def create_feature(name=None):
    """Crea una nuova feature"""
    global _current_feature
    _current_feature = BDDFeature(name)


def create_scenario(name=None):
    """Crea un nuovo scenario"""
    global _current_scenario
    _current_scenario = BDDScenario(name)


def add_passed_step(name=None):
    """Aggiunge uno step passato allo scenario corrente"""
    step = create_passed_step(name)
    _current_scenario.add_step(step)


def add_failed_step(name=None):
    """Aggiunge uno step fallito allo scenario corrente"""
    step = create_failed_step(name)
    _current_scenario.add_step(step)


def add_skipped_step(name=None):
    """Aggiunge uno step skippato allo scenario corrente"""
    step = create_skipped_step(name)
    _current_scenario.add_step(step)


def attach_scenario_to_feature():
    """Collega lo scenario corrente alla feature corrente"""
    _current_feature.add_scenario(_current_scenario)


def attach_feature_to_builder():
    """Collega la feature corrente al builder"""
    _builder.add_feature(_current_feature)


def build_tests():
    """Genera i file di test"""
    _builder.build()
