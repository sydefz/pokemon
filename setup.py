try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="pokemonscanner",
    author="Xinyang Zhang",
    author_email="paul@freelancer.com",
    version=0.1,
    description="Pokemon Go Scanner",
    install_requires=[
        'attrs==16.0.0',
        'cffi==1.7.0',
        'cryptography==1.4',
        'cssselect==0.9.2',
        'idna==2.1',
        'lxml==3.6.1',
        'parsel==1.0.2',
        'pyasn1==0.1.9',
        'pyasn1-modules==0.0.8',
        'pycparser==2.14',
        'PyDispatcher==2.0.5',
        'pyglet==1.2.4',
        'pyOpenSSL==16.0.0',
        'queuelib==1.4.2',
        'Scrapy==1.1.1',
        'service-identity==16.0.0',
        'six==1.10.0',
        'Twisted==16.3.0',
        'w3lib==1.14.3',
        'zope.interface==4.2.0'
    ],
    zip_safe=False,
    debian_build_deps=[],
    packages=find_packages(),
    include_package_data=True,
)