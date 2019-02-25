#!/bin/bash

# Builds and uploads a new version.
# You have to manually update the version number in `setup.py` first!

echo 'Did you update the version number in setup.py?'
python setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

