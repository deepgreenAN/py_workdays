from setuptools import setup

install_requires = [
    "jpholiday",
    "pytz"
    "numpy",
    "pandas",
    "requests",
    "py-strict-list @ git+https://github.com/deepgreenAN/py_strict_list@master#egg=py-strict-list"
]
packages = [
    "py_workdays"
]

setup(
    name='py-workdays',
    version='0.0.0',
    packages=packages,
    install_requires=install_requires,
)