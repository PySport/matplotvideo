""" matplotvideo is a Python package providing an easy way to sync video to matplotlib
"""

DOCLINES = (__doc__ or '').split("\n")
from distutils.core import setup

import setuptools

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='matplotvideo',
    version='0.0.1',
    author='Koen Vossen',
    author_email='info@koenvossen.nl',
    url="https://github.com/PySport/matplotvideo",
    packages=setuptools.find_packages(exclude=["test", "examples"]),
    license='MIT',
    description="Syncing matplotlib and video",
    long_description="\n".join(DOCLINES),
    python_requires='>=3.7',
    #install_requires=[],
    # extras_require={
    #     'dev': [
    #         'pytest'
    #     ]
    # }
)
