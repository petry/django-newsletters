import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-newletters",
    version = "0.2",
    url = 'https://github.com/petry/django-newsletters',
    license = 'BSD',
    description = "A pressroom application for django.",
    long_description = read('README'),

    author = 'Marcos Daniel Petry',
    author_email = 'marcospetry@gmail.com',

    packages = find_packages('newsletters'),
    package_dir = {'': 'newsletters'},

    install_requires = ['setuptools', 'django-newsletters'],

    classifiers = [
        'Development Status :: 4.1 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
