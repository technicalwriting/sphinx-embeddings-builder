working_directory=$(pwd)

if [ ! -d ~/.venv ]; then
    mkdir ~/.venv
fi

if [ ! -d ~/.venv/sphinx-embeddings-builder ]; then
    python3 -m venv ~/.venv/sphinx-embeddings-builder
fi

if [ ! -d /tmp/sphinx ]; then
    cd /tmp
    git clone --depth 1 git@github.com:sphinx-doc/sphinx.git
fi

source ~/.venv/sphinx-embeddings-builder/bin/activate
cd /tmp/sphinx
python3 -m pip uninstall --yes sphinx-embeddings-builder
python3 -m pip install sphinx-embeddings-builder
python3 -m pip install -U sphinx-embeddings-builder
python3 -m pip install -e .
# TODO: Replace `html` with `embeddings`
# https://www.sphinx-doc.org/en/master/man/sphinx-build.html#cmdoption-sphinx-build-E
sphinx-build -M html ./doc ./build/sphinx -W --keep-going -E
deactivate
cd $working_directory
