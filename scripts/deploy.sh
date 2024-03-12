# Get the latest tag
latest_tag=$(git describe --tags)

latest_tag=${latest_tag#v}

echo $latest_tag
echo `pwd`
echo `ls wall`

sed -i '' -e "s/version = \".*\"/version = \"$latest_tag\"/g" wall/pyproject.toml || exit 1
sed -i '' -e "s/version = \".*\"/version = \"$latest_tag\"/g" drawbridge/pyproject.toml || exit 1

python3 -m pip install --upgrade twine
cd wall && python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST && cd ..
cd drawbridge && python3 -m twine upload --repository testpypi dist/*  --non-interactive --username __token__ --password $PYPI_PASSWORD_TEST