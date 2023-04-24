from setuptools import setup, find_packages

def install_requires():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

# TODO: Make it possible to use the builder without modifying the extensions list.
# https://www.sphinx-doc.org/en/master/development/builders.html
setup(
    name='sphinx-embeddings-builder',
    version='0.1',
    packages=find_packages(),
    install_requires=install_requires(),
    classifiers=[],
    entry_points={
        'sphinx.builders': [
            'embeddings = sphinx-embeddings-builder'
        ]
    }
)
