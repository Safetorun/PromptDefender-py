python scripts/set_version.py
python3 -m pip install --upgrade twine build

# Build
cd wall && python3 -m build && cd ..
cd drawbridge && python3 -m build

# Deploy
cd wall && python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST && cd ..
cd drawbridge && python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST