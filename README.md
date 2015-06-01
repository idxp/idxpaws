# pyidxp

[![Build Status](https://travis-ci.org/idxp/pyidxp.svg?branch=master)](https://travis-ci.org/idxp/pyidxp) [![Code Climate](https://codeclimate.com/github/idxp/pyidxp/badges/gpa.svg)](https://codeclimate.com/github/idxp/pyidxp) [![PyPI Version](https://img.shields.io/pypi/v/pyidxp.svg?style=flat)](https://pypi.python.org/pypi/pyidxp/) [![Dependency Status](https://gemnasium.com/idxp/pyidxp.svg)](https://gemnasium.com/idxp/pyidxp)

Simple libs for AWS services. Python 3.4 is required.

## Publishing to PyPI

Install `wheel`

```
pip install wheel
```

Register the application

```
python setup.py register
```

Generate the archives

```
python setup.py sdist bdist_wheel
```

Upload them to PyPI

```
python setup.py sdist bdist_wheel upload
```

Party!
