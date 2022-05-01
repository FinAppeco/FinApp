import setuptools

setuptools.setup(
    name="app",
    packages=setuptools.find_packages(exclude=["finapp_tests"]),
    install_requires=[
        "dagster==0.12.14",
        "dagit==0.12.14",
        "pytest",
    ],
)
