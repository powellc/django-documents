#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Dynamically calculate the version based on documents.VERSION
version_tuple = __import__('documents').VERSION
if len(version_tuple) == 3:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    name = "django-documents",
    version = version,
    description = "documents management for the Django web framework.",
    author = "Colin Powell",
    author_email = "cpowel@penobscotbaypress.com",
    url = "http://src.coastalconnect.me/django-documents/",
    packages = find_packages(),
    package_data = {
        'documents': [
            'templates/documents/*.html',
        ]
    },
    zip_safe = False,
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)

