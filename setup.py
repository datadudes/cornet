from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cornet',
    version='0.1.3',
    author='Marcel Krcah, Daan Debie',
    author_email='marcel.krcah@gmail.com, debie.daan@gmail.com',
    description='Easily generate Apache Sqoop commands based on YAML config file',
    license='MIT',
    keywords='sqoop yaml hadoop hive mysql postgresql',
    url='https://github.com/datadudes/cornet',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['cornet=cornet.main:cli']
    },
    extras_require={
        'mysql': ['mysqlclient==1.3.5'],
        'postgres': ['psycopg2==2.6'],
    },
    install_requires=requirements,
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Utilities',
    ]
)
