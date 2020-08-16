import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='rest_tracker',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Django app to easily track and store views request and responses',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/tannerburns/rest_tracker',
    author='Tanner Burns',
    author_email='tjburns102@gmail.com',
    install_requires=[
        'django'
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django-Rest-Framework',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)