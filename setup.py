from setuptools import setup

setup(
    name='helixpc',
    version='1.0.2',
    license='MIT',
    description='Automisation of graph generation for gene FC databases.',
    long_description=open('README.rst').read(),
    author='Anne-Laure Ehresmann',
    author_email='cathaspa@protonmail.com',
    url='https://github.com/Cathaspa/HelixPC',
    packages=['helixpc'],
    entry_points = {
        'console_scripts': ['helixpc=helixpc.cli:main']
        },
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
    ]
)
