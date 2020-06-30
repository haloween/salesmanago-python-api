# salesmanago-python-api
Python API for SalesManago integration.

# Installation
Install this library in a virtualenv using pip. virtualenv is a tool to create isolated Python environments. The basic problem it addresses is one of dependencies and versions, and indirectly permissions.

With virtualenv, it's possible to install this library without needing system install permissions, and without clashing with the installed system dependencies.

# Mac/Linux
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install salesmanago_python_api

# Windows
pip install virtualenv
virtualenv <your-env>
<your-env>\Scripts\activate
<your-env>\Scripts\pip.exe install salesmanago_python_api

# Supported Python Versions
Python 3.7, and 3.8 are fully supported and tested. This library may work on later versions of 3, but we do not currently run tests against those versions

Deprecated Python Versions
Python <= 3.7

# Third Party Libraries and Dependencies
The following libraries will be installed when you install the client library:

requests
