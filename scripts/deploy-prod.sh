cd "$1"
python3 -m pip install --upgrade twine build

# Build
python3 -m build

# Deploy
python3 -m twine upload --repository pypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD && cd ..
