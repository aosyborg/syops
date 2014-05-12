from setuptools import setup, find_packages

setup(
    name='syopsui',
    version='0.0.1-1',
    description='Web code for SyOps',
    long_description='Web code for SyOps',
    author='Dave Symons',
    author_email='symons@aospace.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyramid',
        'pyramid_chameleon',
        'pyramid_debugtoolbar',
        'pyramid_beaker',
        'simplejson==3.1.0',
        'waitress',
        'psycopg2',
        'ConfigParser'
    ],
    scripts=[],
    entry_points="""\
    [paste.app_factory]
    main = syopsui:main
    """,
)

