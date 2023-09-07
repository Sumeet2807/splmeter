# setup.py
import setuptools

setuptools.setup(
    name="SPLmeter",
    version="0.0.4",
    author="Sumeet",
    author_email="s.saini@ufl.edu",
    description="splmeter for acoustic measurement using python",
    packages=setuptools.find_packages(),
    install_requires=['numpy','plotly','schemdraw','scipy']
)