python3 -m pip install --upgrade build poetry || exit 1
cd $1 || exit 1
python3 -m build || exit 1