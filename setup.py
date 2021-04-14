import setuptools
import os

def git_hash():
    if os.path.exists('.git/FETCH_HEAD'):
        return '+' + open('.git/FETCH_HEAD').read().split()[0]
    return ''

setuptools.setup(
    name='PyMongoWrapper',
    version='0.1.4' + git_hash(),
    keywords='mongodb',
    description='Python wrapper for MongoDB based on PyMongo',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='zhuth',
    author_email='zthpublic@gmail.com',
    url='https://github.com/zhuth/PyMongoWrapper',
    packages=setuptools.find_packages(),
    requires=['pymongo'],
    license='MIT'
)