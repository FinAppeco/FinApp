import setuptools

setuptools.setup(
    name="app",
    packages=setuptools.find_packages(exclude=["finapp_tests"]),
    install_requires=[
        "pytest",
        "pandas==1.3.3",
        "dagster==0.12.14",
        "dagster-graphql==0.12.14",
        "dagit==0.12.14",
        "dagster-postgres==0.12.14",
        "dagster-docker==0.12.14",
        "dagster-gcp==0.12.14",
        "dagstermill==0.12.14",
        "gcsfs==2022.2.0",
        "dateparser==1.0.0",
        "db-dtypes",
        "python-decouple==3.4",
        "mplfinance==0.12.8b9",
        "openpyxl==3.0.7",
        "finnhub-python==2.4.13",
        "markupsafe==2.0.1",
        "jupyter"
    ],
)
