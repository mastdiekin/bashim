from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name = 'bashim-cli',
    version = '0.1.0',
    packages = find_packages(),
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'bashim = src.bashim:main'
        ]
    }
)