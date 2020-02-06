from setuptools import setup, find_packages

required = [
    "pip>=18.0",
    "joblib",
    "requests",
    "path"
]


setup(
    name="catalogue",
    version="0.01",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "pycat=catalogue:cli"
            # more script entry points ...
        ]
    }
)