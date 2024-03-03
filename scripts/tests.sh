set -e

pytest -v
python -m coverage run -m pytest
python -m coverage report -m