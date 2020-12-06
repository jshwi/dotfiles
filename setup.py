"""
setup
=====

``setuptools`` for package.
"""
import setuptools

__name__ = "dotfiles"
__author__ = "Stephen Whitlock"
__email__ = "stephen@jshwisolutions.com"
__copyright__ = "2020, Stephen Whitlock"
__license__ = "MIT"
__version__ = "1.0.0"

with open("README.rst") as file:
    README = file.read()


setuptools.setup(
    name=__name__,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    version=__version__,
    license=__license__,
    description="My dotfiles",
    long_description=README,
    platforms="GNU/Linux",
    long_description_content_type="text/x-rst",
    url="https://github.com/jshwi/jshwisolutions",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="bash zsh home dotfiles python",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires=">=3.9",
)
