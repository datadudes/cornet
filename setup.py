from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="sisyphus",
    version="0.1-SNAPSHOT",
    author="Marcel Krcah, Daan Debie",
    author_email="marcel.krcah@gmail.com, debie.daan@gmail.com",
    description="Easily generate Apache Sqoop commands based on YAML config file",
    license="MIT",
    keywords="sqoop yaml hadoop hive",
    url="https://github.com/datadudes/sisyphus",
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['sisyphus=sisyphus.main:cli']},
    extras_require={
        'mysql': ["mysqlclient==1.3.5"],
        'postgres': ["psycopg2==2.6"],
    },
    install_requires=requirements
)