from distutils.core import setup

import setuptools

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='matplotvideo',
    version='0.0.2',
    author='Koen Vossen',
    author_email='info@koenvossen.nl',
    url="https://github.com/PySport/matplotvideo",
    packages=setuptools.find_packages(exclude=["test", "examples"]),
    license='MIT',
    description="Syncing matplotlib and video",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Framework :: Matplotlib"
    ]
)
