# SyOps

## Installation
1. Clone the repository
```
    git clone git@github.com:aosyborg/syops.git
```

1. Install a virtual environment
```
    # From project root
    virtualenv env --no-site-packages
```

1. Install SyOps into the virtual environment
```
    # From project root
    source env/bin/activate
    python setup.py develop
```

1. Install the DB
```
    # From syops/db/releases
    psql -h yourhost -U postgres yourdb < 0.1.sql
```

1. Activate the UI
```
    # From project root
   ./env/bin/pserve development.ini --reload
```

1. Activate the MW
```
    # From syops/mw (besure your virtual env is activated)
    python start.py
```
