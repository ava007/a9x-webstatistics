import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='a9x_webstatistics',
    author='André von Arx',
    author_email='andrevonarx@bluewin.ch',
    description='Web Statistics and Analytics Package',
    keywords='webstats, statistics, analytics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ava007/a9x-webstatistics',
    project_urls={
        'Documentation': 'https://github.com/ava007/a9x-webstatistics',
        'Bug Reports':
        'https://github.com/ava007/a9x-webstatistics/issues',
        'Source Code': 'https://github.com/ava007/a9x-webstatistics',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=['geoip2'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
