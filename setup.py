from setuptools import setup, find_packages

def install_requires():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

setup(
    name='sphinx-embeddings-builder',
    version='0.0.5',
    packages=find_packages(),
    install_requires=install_requires(),
    classifiers=[],
)
