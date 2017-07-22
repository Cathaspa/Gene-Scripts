from setuptools import setup
exec(open('helixpc/_version.py').read())

setup(
    name='helixpc',
    version=__version__,
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
