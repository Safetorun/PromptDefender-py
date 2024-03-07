python3 -m pip install --upgrade twine
cd wall && python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST
