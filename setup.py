import os

from setuptools import find_packages, setup

NAME = "ellipsoid_orientation"
here = os.path.abspath(os.path.dirname(__file__))
__version__ = "0.0.1"
setup(
    name=NAME,
    version=__version__,
    description="Helpful functions used in the CME lab",
    url="https://github.com/cmelab/ellipsoid_orientations",
    author="CME Lab",
    author_email="marjanalbooyeh@u.boisestate.edu",
    license="GPLv3",
    packages=find_packages(),
    package_dir={"src": "*.py"},
    zip_safe=False,
)