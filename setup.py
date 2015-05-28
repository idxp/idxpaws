from setuptools import setup, find_packages

setup(
    name='Idxpaws',
    version='0.1.1',
    author='Artur Rodrigues, Denis Lins',
    author_email='arturhoo@gmail.com, denis.lins@outlook.com',
    description='IDXP AWS - Simple libs for AWS services',
    url='https://github.com/idxp/idxpaws',
    download_url='https://github.com/idxp/idxpaws/tarball/0.1.1',
    license='LICENSE',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'boto >= 2.36'
    ],
    tests_require=['pytest'],
)
