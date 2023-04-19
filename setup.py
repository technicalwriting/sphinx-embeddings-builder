from setuptools import setup, find_packages

def install_requires():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]

setup(
    name='sphinx-embeddings',
    version='0.1',
    packages=find_packages(),
    install_requires=install_requires(),
    classifiers=[],
)
