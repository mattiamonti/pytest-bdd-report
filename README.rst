=================
pytest-bdd-report
=================

|python| |pypi| |formatting|

|tests| |bdd_tests| |ui_tests|

|total|

.. |total| image:: https://static.pepy.tech/badge/pytest-bdd-report
    :target: https://pepy.tech/project/pytest-bdd-report
    :alt: PePy total downloads

.. |pypi| image:: https://img.shields.io/pypi/v/pytest-bdd-report.svg
    :target: https://pypi.org/project/pytest-bdd-report
    :alt: PyPI version

.. |python| image:: https://img.shields.io/pypi/pyversions/pytest-bdd-report.svg
    :target: https://pypi.org/project/pytest-bdd-report
    :alt: Python versions

.. |formatting| image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/black.yml?logo=GitHub%20actions&label=Formatting
    :alt: GitHub Workflow Status (with event)

.. |tests| image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/unit%20tests.yml?logo=pytest&label=Unit%20Tests
    :alt: GitHub Workflow Status (with event)

.. |bdd_tests| image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/ui%20BDD%20tests.yml?logo=pytest&label=BDD%20UI%20Tests
    :alt: GitHub Workflow Status (with event)

.. |ui_tests| image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/ui%20automated%20tests.yml?logo=robotframework&label=UI%20Tests
    :alt: GitHub Workflow Status (with event)

.. |dstats| image:: https://img.shields.io/pypi/dd/pytest-bdd-report
   :alt: PyPI - Downloads



The `pytest-bdd-report` plugin is an extension for the `pytest-bdd`_ library that generates clear, interactive HTML reports for BDD (Behavior-Driven Development) tests. It provides a comprehensive view of test executions, making it easy for developers, testers, and stakeholders to understand test results.

For detailed guides and examples, check out the `Documentation`_.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* **Detailed BDD Reports**: Generate comprehensive reports showing executed steps, scenarios, and results.
* **Interactive HTML Format**: View test results in an intuitive, easy-to-navigate HTML report.
* **Rich Attachments**: Enrich reports with screenshots, text notes, and JSON data attached to specific steps or scenarios.
* **Quick Setup**: Install and start generating reports in minutes.


Requirements
------------

* Jinja2
* pytest
* pytest-bdd


Installation
------------

Install the plugin via pip:

::

    $ pip install pytest-bdd-report

Make sure you have `pytest`_ and `pytest-bdd`_ installed in your environment.


Usage
-----

Generate an HTML report by running:

::

    $ pytest --bdd-report="report.html"

This command creates a detailed report file at the specified path.


Enriching Reports with Attachments
----------------------------------

The plugin provides three helper functions in the ``pytest_bdd_report.attach`` module to enrich your reports with additional context and evidence.

1. Attach Screenshots
=====================

Add screenshots to scenarios using ``attach.screenshot()``. Accepts raw bytes (e.g., from Playwright) or file paths.

.. code-block:: python

    from pytest_bdd_report import attach

    # From raw bytes (e.g., Playwright)
    screenshot_bytes = page.screenshot()
    attach.screenshot(screenshot_bytes, feature_name="Login", scenario_name="Successful login")

    # From file path
    attach.screenshot("screenshots/test.png", feature_name="Login", scenario_name="Successful login")

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``image``
     - ``bytes | str | Path``
     - Screenshot content as raw bytes or file path.
   * - ``feature_name``
     - ``str``
     - Name of the feature containing the scenario.
   * - ``scenario_name``
     - ``str``
     - Name of the scenario to attach the screenshot to.

2. Attach Text to Steps
=======================

Add textual notes to specific steps using ``attach.text_to_step()``. Call it multiple times on the same step to attach multiple notes.

.. code-block:: python

    from pytest_bdd import given
    from pytest_bdd_report import attach

    @given("I am on the login page")
    def setup_login():
        attach.text_to_step(
            "User navigated to /login",
            step_keyword="Given",
            step_name="I am on the login page"
        )

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``text``
     - ``str``
     - The text content to attach.
   * - ``step_keyword``
     - ``str``
     - BDD keyword (e.g., "Given", "When", "And", "Then").
   * - ``step_name``
     - ``str``
     - The step name/description.

3. Attach JSON to Steps
=======================

Attach structured data (e.g., API responses, test fixtures) to steps using ``attach.json_to_step()``. Multiple JSON objects can be attached to the same step.

.. code-block:: python

    from pytest_bdd import when
    from pytest_bdd_report import attach

    @when("I fetch user data")
    def fetch_user_data():
        user_data = {"id": 123, "name": "John", "role": "admin"}
        attach.json_to_step(
            user_data,
            step_keyword="When",
            step_name="I fetch user data"
        )

**Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Type
     - Description
   * - ``data``
     - ``dict``
     - The JSON/dict data to attach.
   * - ``step_keyword``
     - ``str``
     - BDD keyword (e.g., "Given", "When", "And", "Then").
   * - ``step_name``
     - ``str``
     - The step name/description.

Example: Automatic Screenshots Attachments on Playwright Failure
==========================================

Use pytest-bdd hooks to automatically capture screenshots when a step fails:

.. code-block:: python

    import pytest
    from pytest_bdd_report import attach

    @pytest.hookimpl(hookwrapper=True)
    def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
        yield
        for fixture in step_func_args.values():
            page = getattr(fixture, "page", None)
            if page:
                # Attach screenshot from bytes
                screenshot_bytes = page.screenshot()
                attach.screenshot(screenshot_bytes, feature.name, scenario.name)

                # Or attach from file path
                screenshot_path = "screenshots/error.png"
                page.screenshot(path=screenshot_path)
                attach.screenshot(screenshot_path, feature.name, scenario.name)


Running Tests
-------------

To run the plugin's own tests:

1. Create a virtual environment and install dependencies:

::

    $ pip install -r requirements.txt
    $ playwright install


2. Install the plugin in editable mode:

::

    $ pip install -e .


3. Run unit tests:

::

    $ python -m pytest --ignore=tests/bdd/


4. Run BDD UI tests:

::

    $ python -m pytest tests/bdd


5. Generate a report for the BDD tests:

::

    $ python -m pytest tests/bdd --bdd-report="report.html"


Contributing
------------

Contributions are welcome! Please run tests before submitting a pull request using the commands shown above.


License
-------

Distributed under the terms of the `MIT`_ license. "pytest-bdd-report" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/mattiamonti/pytest-bdd-report/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-bdd`: https://github.com/pytest-dev/pytest-bdd
.. _`Documentation`: https://mattia-monti.gitbook.io/pytest-bdd-report/
