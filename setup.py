try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="pokemonscanner",
    author="Xinyang Zhang",
    author_email="sydefz@gmail.com",
    version=0.1,
    description="Pokemon Go Scanner",
    install_requires=[
        'pyglet==1.2.4',
        'cfscrape==1.6.6'
    ],
    zip_safe=False,
    debian_build_deps=[],
    packages=find_packages(),
    include_package_data=True,
)