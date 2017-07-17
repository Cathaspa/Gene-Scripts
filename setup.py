from setuptools import setup, find_packages

setup(
    name='helixsj',
    version='1.0.0',
    license='MIT',
    description='Automisation of graph generation for gene FC databases.',
    long_description=open('README.rst').read(),
    author='Anne-Laure Ehresmann',
    author_email='cathaspa@protonmail.com',
    url='https://github.com/Cathaspa/HelixSJ',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
    ]
)
