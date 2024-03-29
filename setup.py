import setuptools
import os


def git_hash():
    op = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '.git', 'FETCH_HEAD')
    if os.path.exists(op):
        return '+' + open(op).read().split()[0][-8:]
    return ''


setuptools.setup(
    name='PyMongoWrapper',
    version='0.3.0' + git_hash(),
    keywords='mongodb',
    description='Python wrapper for MongoDB based on PyMongo',
    long_description_content_type='text/markdown',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        ),
        encoding='utf-8'
    ).read(),
    author='zhuth',
    author_email='zthpublic@gmail.com',
    url='https://github.com/zhuth/PyMongoWrapper',
    packages=setuptools.find_namespace_packages(),
    install_requires=['pymongo', 'antlr4-python3-runtime'],
    license='MIT'
)
