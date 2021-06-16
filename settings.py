from os import environ, path
import yaml

basedir = path.abspath(path.dirname(__file__))

try:
    with open('conf.yaml') as config:
        keys = yaml.safe_load(config)
        PSQL_username = keys.get('PSQL_username')
        PSQL_password = keys.get('PSQL_password')
        PSQL_address = keys.get('PSQL_address')
        PSQL_port = keys.get('PSQL_port')
        PSQL_DB = keys.get('PSQL_DB')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PSQL_username}:{PSQL_password}@{PSQL_address}:{PSQL_port}/{PSQL_DB}"
    SQLALCHEMY_MIGRATE_REPO = path.join(basedir, 'migrations')
except FileNotFoundError:
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')