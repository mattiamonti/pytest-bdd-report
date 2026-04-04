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



The `pytest-bdd-report` plugin is a useful extension for the `pytest-bdd`_ library that allows you to generate
useful and informative reports for BDD (Behavior-Driven Development) tests developed using the pytest-bdd framework.
This plugin facilitates the generation of clear and effective HTML reports, providing a comprehensible view of BDD test executions within the project.

For more, check out the `Documentation`_

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* **Detailed BDD Reports**: The pytest-bdd-report plugin enables the generation of detailed reports for BDD tests executed using pytest-bdd. These reports clearly show the executed steps, tested scenarios, and obtained results.
* **HTML Format**: The generated reports are presented in an intuitive and interactive HTML format. This allows developers, testers, and other team members to easily view the status of BDD tests.
* **Easy Installation**: Installing the plugin is simple and fast. You can install it using the command `pip install pytest-bdd-report`.


Requirements
------------

* Jinja2
* pytest
* pytest-bdd


Installation
------------

1. Ensure that you have `pytest`_ and `pytest-bdd`_ installed in your development environment.
2. Open a terminal window.
3. Execute the following command to install the `pytest-bdd-report` plugin via `pip`_ from `PyPI`_

::

    $ pip install pytest-bdd-report


Usage
-----

Once installed, you can generate BDD reports in an HTML file using the following command:

::

    $ pytest --bdd-report="report.html"

Attachments
-----------

You can enrich your HTML reports by attaching screenshots, text, and JSON data to specific steps or scenarios. The plugin provides three helper functions in the ``pytest_bdd_report.attach`` module.

Attach Screenshots
==================

Use ``attach.screenshot()`` to add screenshots to a specific scenario in the report. This function accepts either raw bytes (e.g., from Playwright's ``page.screenshot()``) or a file path to an image.

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
     - Screenshot content. Can be raw bytes or a file path to the image.
   * - ``feature_name``
     - ``str``
     - The name of the feature to which the screenshot belongs.
   * - ``scenario_name``
     - ``str``
     - The name of the scenario to which the screenshot belongs.

Attach Text to Steps
====================

Use ``attach.text_to_step()`` to add textual information to a specific step. You can call this method multiple times on the same step to attach multiple pieces of text.

.. code-block:: python

    from pytest_bdd import given
    from pytest_bdd_report import attach

    @given("I am on the login page")
    def setup_login():
        # Step implementation...
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
     - The text content to attach to the step.
   * - ``step_keyword``
     - ``str``
     - The BDD keyword of the step (e.g., "Given", "When", "And", "Then").
   * - ``step_name``
     - ``str``
     - The name/description of the step.

Attach JSON to Steps
====================

Use ``attach.json_to_step()`` to attach structured JSON data to a specific step. This is useful for attaching API responses, configuration data, or test fixtures. Like text, you can attach multiple JSON objects to the same step.

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
     - The JSON/dict data to attach to the step.
   * - ``step_keyword``
     - ``str``
     - The BDD keyword of the step (e.g., "Given", "When", "And", "Then").
   * - ``step_name``
     - ``str``
     - The name/description of the step.

Complete Example with Playwright
================================

Here's a complete example showing how to attach screenshots on test failure using pytest-bdd hooks:

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



Run tests
---------

To run tests:

1. Create a virtual environment
2. Install the required packages:

::

    $ pip install -r requirements.txt
    $ playwright install


3. Install the plugin locally:

::

    $ pip install -e .


4. Run the unit tests:

::

    $ python -m pytest --ignore=tests/bdd/

5. Run the BDD UI tests with pytest-bdd:

::

    $ python -m pytest tests/bdd

6. Want a report for the Playwright BDD tests? use the --bdd-report flag!

::

    $ python -m pytest tests/bdd --bdd-report="report.html"


Contributing
------------
Contributions are very welcome. Tests can be run with `pytest`_ as shown.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-bdd-report" is free and open source software


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
