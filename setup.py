import setuptools
import os, glob, shutil

BASE = os.path.dirname(__file__)
os.chdir(BASE)
os.mkdir('PyMongoWrapper')

for g in glob.glob('*.py'):
    shutil.copy(g, 'PyMongoWrapper')

setuptools.setup(
    name='PyMongoWrapper',
    version='0.1.3',
    keywords='mongodb',
    description='Python wrapper for MongoDB based on PyMongo',
    long_description=open(
        os.path.join(
            BASE,
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