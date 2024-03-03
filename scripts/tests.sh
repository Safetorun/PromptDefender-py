set -e

source wall/venv/bin/activate
pytest -v
python -m coverage run -m pytest
python -m coverage report -m