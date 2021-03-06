import setuptools
import os

setuptools.setup(
    name='PyMongoWrapper',
    version='0.1.1',
    keywords='mongodb',
    description='Python wrapper for MongoDB based on PyMongo',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='zhuth',
    author_email='thzhu@139.com',
    url='https://github.com/zhuth/PyMongoWrapper',
    packages=setuptools.find_packages(),
    requires=['pymongo'],
    license='MIT'
)