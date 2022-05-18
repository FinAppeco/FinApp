import setuptools

setuptools.setup(
    name="app",
    packages=setuptools.find_packages(exclude=["finapp_tests"]),
    install_requires=[
        "pytest",
        "pandas==1.3.3",
        "dagster==0.14.15",
        "dagster-graphql==0.14.15",
        "dagit==0.14.15",
        "dagster-postgres==0.14.15",
        "dagster-docker==0.14.15",
        "dagster-gcp==0.14.15",
        "dagstermill==0.14.15",
        "gcsfs==2022.3.0",
        "dateparser==1.0.0",
        "db-dtypes",
        "python-decouple==3.5",
        "mplfinance==0.12.8b9",
        "openpyxl==3.0.9",
        "finnhub-python==2.4.13",
        "markupsafe==2.0.1",
        "jupyter"
    ],
)
