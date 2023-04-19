source venv/bin/activate
python3 -m pip install setuptools wheel twine
python3 setup.py sdist bdist_wheel
twine upload dist/*
