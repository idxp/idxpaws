# pyidxp

[![Build Status](https://travis-ci.org/idxp/idxpaws.svg?branch=master)](https://travis-ci.org/idxp/idxpaws) [![Code Climate](https://codeclimate.com/github/idxp/idxpaws/badges/gpa.svg)](https://codeclimate.com/github/idxp/idxpaws) [![PyPI Version](https://img.shields.io/pypi/v/Idxpaws.svg?style=flat)](https://pypi.python.org/pypi/Idxpaws/) [![Dependency Status](https://gemnasium.com/idxp/idxpaws.svg)](https://gemnasium.com/idxp/idxpaws)

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
python setup.py sdist
python setup.py bdist_wheel
```

Upload them to PyPI

```
python setup.py sdist bdist_wheel upload
```

Party!
