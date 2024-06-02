cd "$1"

echo $2

if [ "$2" = "test" ]
then
  REPO="testpypi"
  PASSWORD=$PYPI_PASSWORD_TEST
elif [ "$2" = "prod" ]
  then
  REPO="pypi"
  PASSWORD=$PYPI_PASSWORD
else
  echo "Invalid argument $2. Please use 'test' or 'prod'"
  exit 1
fi

python3 -m twine upload --repository $REPO dist/*  --non-interactive --username __token__ --password $PASSWORD