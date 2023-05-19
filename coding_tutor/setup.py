from setuptools import setup, find_packages

setup(
    name='coding_tutor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'ipywidgets'
    ],
)
