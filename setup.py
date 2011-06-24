#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Dynamically calculate the version based on photologue.VERSION
version_tuple = __import__('newsletters').VERSION
if len(version_tuple) == 3:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    name = "django-newletters",
    version = version,
    description = "A newsletter application for django.",
    author = 'Marcos Daniel Petry',
    author_email = 'marcospetry@gmail.com',
    url = 'https://github.com/petry/django-newsletters',
    packages = find_packages(),
    package_data = {
        'newsletters': [
            'bin/*',
            'fixtures/*'
            'locale/*/LC_MESSAGES/*',
            'templates/newsletters/*.html',
            'templates/admin/newsletters/*.html',
        ]
    },
    zip_safe = False,

    classifiers = [
        'Development Status :: 4.1 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)