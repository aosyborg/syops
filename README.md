# SyOps

Be sure to read the wiki!

## Installation
1. Clone the repository
```
    git clone git@github.com:aosyborg/syops.git
```

2. Install a virtual environment
```
    # From project root
    virtualenv env --no-site-packages
```

3. Install SyOps into the virtual environment
```
    # From project root
    source env/bin/activate
    python setup.py develop
```

4. Install the DB
```
    # From syops/db/releases
    psql -h yourhost -U postgres yourdb < 0.1.sql
```

5. Activate the UI
```
    # From project root
   ./env/bin/pserve development.ini --reload
```

6. Activate the MW
```
    # From syops/mw (besure your virtual env is activated)
    python start.py
```
