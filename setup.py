from setuptools import setup, find_packages

setup(
    name='syops',
    version='0.0.1-1',
    description='DevOps made easy with github and aws',
    long_description='DevOps made easy with github and aws',
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
        'ConfigParser',
        'boto'  # AWS SDK
    ],
    scripts=[],
    entry_points="""\
    [paste.app_factory]
    main = syops.ui:main
    """,
)

