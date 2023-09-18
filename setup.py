from setuptools import setup, find_packages

setup(
    name="springchallenge2023",
    version="0.3",
    install_requires=["gymnasium==0.29.0"],
    packages = find_packages(where='springchallenge2023'),
    package_dir = {'': 'springchallenge2023'},
)
