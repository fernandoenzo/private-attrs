# encoding:utf-8

# More on how to configure this file here: https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
import setuptools
from setuptools import find_packages

name = 'private-attrs'

# https://www.python.org/dev/peps/pep-0440/#version-scheme
version = '1.0.0'

description = "This module provides support for easy addition of private attributes inside your custom objects, " \
              "which are totally unreachable from outside the class definition, as in C++ 'private' clause."

with open("README.md", "r") as fh:
    long_description = fh.read()

author = 'Fernando Enzo Guarini'
author_email = 'fernandoenzo@gmail.com'

url = 'https://github.com/fernandoenzo/private-attrs/'

# https://packaging.python.org/guides/distributing-packages-using-setuptools/#project-urls
project_urls = {
    'Source': 'https://github.com/fernandoenzo/private-attrs/',
}

packages = find_packages(exclude=("tests",))
py_modules = ['private_attrs']
test_suite = 'tests'

license = 'GPLv3+'

zip_safe = True

keywords = 'attr attribute private static'

python_requires = '>=3.7'

# https://pypi.org/classifiers/
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setuptools.setup(
    author_email=author_email,
    author=author,
    classifiers=classifiers,
    description=description,
    download_url=url,
    keywords=keywords,
    license=license,
    long_description_content_type="text/markdown",
    long_description=long_description,
    name=name,
    packages=packages,
    project_urls=project_urls,
    py_modules=py_modules,
    python_requires=python_requires,
    test_suite=test_suite,
    url=url,
    version=version,
    zip_safe=zip_safe,
)
