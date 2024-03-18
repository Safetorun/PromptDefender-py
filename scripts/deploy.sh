python scripts/set_version.py
python3 -m pip install --upgrade twine build

python3 -m build
python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST && cd ..