import setuptools

setuptools.setup(
    name="finapp",
    packages=setuptools.find_packages(exclude=["finapp_tests"]),
    install_requires=[
        "dagster==0.12.14",
        "dagit==0.12.14",
        "pytest",
    ],
)
