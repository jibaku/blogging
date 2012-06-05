from setuptools import setup, find_packages
import os

package = "blogging"
version = __import__('blogging').get_version().replace(' ', '-')

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README','README.rst','README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

setup(
    name = package,
    version = version,
    author = "Fabien Schwob",
    author_email = "fabien@x-phuture.com",
    description = "Yet another django blogging app",
    long_description = get_readme(),
    license = "BSD",
    url = "http://github.com/jibaku/blogging",
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)