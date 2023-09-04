=================
pytest-bdd-report
=================

.. image:: https://img.shields.io/pypi/v/pytest-bdd-report.svg
    :target: https://pypi.org/project/pytest-bdd-report
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-bdd-report.svg
    :target: https://pypi.org/project/pytest-bdd-report
    :alt: Python versions

.. image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/automated%20tests.yml?logo=GitHub%20actions&label=Black%20formatting
    :alt: GitHub Workflow Status (with event)

.. image:: https://img.shields.io/github/actions/workflow/status/mattiamonti/pytest-bdd-report/automated%20tests.yml?logo=pytest&label=Automated%20Tests
    :alt: GitHub Workflow Status (with event)



The `pytest-bdd-report` plugin is a useful extension for the `pytest-bdd`_ library that allows you to generate 
useful and informative reports for BDD (Behavior-Driven Development) tests developed using the pytest-bdd framework.
This plugin facilitates the generation of clear and effective HTML reports, providing a comprehensible view of BDD test executions within the project.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* **Detailed BDD Reports**: The pytest-bdd-report plugin enables the generation of detailed reports for BDD tests executed using pytest-bdd. These reports clearly show the executed steps, tested scenarios, and obtained results.
* **HTML Format**: The generated reports are presented in an intuitive and interactive HTML format. This allows developers, testers, and other team members to easily view the status of BDD tests.
* **Easy Installation**: Installing the plugin is simple and fast. You can install it using the command `pip install pytest-bdd-report`.


Requirements
------------

* TODO


Installation
------------

1. Ensure that you have `pytest`_ and `pytest-bdd`_ installed in your development environment.
2. Open a terminal window.
3. Execute the following command to install the `pytest-bdd-report` plugin via `pip`_ from `PyPI`_

::

    $ pip install pytest-bdd-report


Usage
-----

Once the plugin is installed, you can generate BDD reports in an HTML file using the command

::

    $ pytest --bdd-report="report.html"

In alternative you can save only the raw tests informations in a JSON file using the command

::

    $ pytest --bdd-json

Contributing
------------
Contributions are very welcome. Tests can be run with `pytest`_, please ensure
the coverage at least stays the same before you submit a pull request.

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