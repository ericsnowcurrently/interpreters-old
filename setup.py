from distutils.core import setup, Extension
import os.path

import interpreters


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


#################################################
# Define the package metadata.

NAME = 'interpreters'
VERSION = interpreters.__version__
AUTHOR = 'Eric Snow'
EMAIL = 'ericsnowcurrently@gmail.com'
URL = 'https://github.com/ericsnowcurrently/interpreters'
LICENSE = 'New BSD License'
SUMMARY = "Python-level access to CPython's C-level subinterpreters API."
# DESCRIPTION is dynamically built below.
KEYWORDS = ''
PLATFORMS = []
CLASSIFIERS = [
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License',
        #'Operating System :: OS Independent',
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        ]

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as readme_file:
    DESCRIPTION = readme_file.read()


#################################################
# Set up files.

PACKAGES = []

PACKAGE_DATA = {}

MODULES = ['interpreters.py']

EXTENSIONS = [
        Extension('_interpreters',
                  ['src/_interpretersmodule.c'],
                  include_dirs=['include'],
                  #define_macros=[('NDEBUG', '1')],
                  #undef_macros=['HAVE_FOO'],
                  ),
        ],


#################################################
# Set up the rest of the package info.

REQUIRES = []


#################################################
# Pull it all together.

kwargs = {'name': NAME,
          'version': VERSION,
          'author': AUTHOR,
          'author_email': EMAIL,
          #'maintainer': MAINTAINER,
          #'maintainer_email': MAINTAINER_EMAIL,
          'url': URL,
          #'download_url': DOWNLOAD,
          'license': LICENSE,
          'description': SUMMARY,
          'long_description': DESCRIPTION,

          'keywords': KEYWORDS,
          'platforms': PLATFORMS,
          'classifiers': CLASSIFIERS,

          'requires': REQUIRES,

          'packages': PACKAGES,
          'package_data': PACKAGE_DATA,
          'py_modules': MODULES,
          'ext_modules': EXTENSIONS,
          }

for key in list(kwargs):
    if not kwargs[key]:
        del kwargs[key]


if __name__ == '__main__':
    if {'src', 'include'} - set(os.listdir(PROJECT_ROOT)):
        raise Exception('missing extension module files; '
                        'please run python3 -m update')
    setup(**kwargs)
