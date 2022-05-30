import setuptools

setuptools.setup(
    name="finapp",
    packages=setuptools.find_packages(exclude=["finapp_tests"]),
    version = "0.0.1",
    author = "Christian Picon",
    author_email = "christian91mp@gmail.com",
    description = ("An data application template to orchestrate dataflows and manage data"),
    license = "BSD",
    keywords = "Dagster Dagit ETL"
)

