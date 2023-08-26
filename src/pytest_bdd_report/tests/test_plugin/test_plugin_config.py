import pytest


def test_plugin_options(pytestconfig):
    pytestconfig.option.saveit = True
    assert pytestconfig.option.saveit
