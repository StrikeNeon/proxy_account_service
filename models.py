from datetime import datetime
from sqlalchemy import BigInteger, String, JSON, DateTime, Integer
from . import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(BigInteger, primary_key=True,
                   autoincrement=True, nullable=False)
    login = db.Column(String(length=200), nullable=False)
    password = db.Column(String(length=200), nullable=False)
    resource = db.Column(BigInteger, db.ForeignKey("resources.id"), nullable=False)
    api_key = db.Column(String(length=200))
    email = db.Column(String(length=200))
    phone = db.Column(String(length=20))
    name = db.Column(String(length=50))
    account_lock = db.relationship("Lock", uselist=False, backref="accounts")

    def __repr__(self):
        return f'{self.id} {self.login}:{self.password}'


class Proxy(db.Model):
    __tablename__ = 'proxies'

    id = db.Column(BigInteger, primary_key=True,
                   autoincrement=True, nullable=False)
    ip_address = db.Column(String(length=15), nullable=False)
    port = db.Column(Integer, nullable=False)
    username = db.Column(String(length=200), nullable=False)
    password = db.Column(String(length=200), nullable=False)
    ip_version = db.Column(String(length=5), nullable=False)
    renewed_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(DateTime)
    valid_resources = db.Column(JSON)
    proxy_lock = db.relationship("Lock", uselist=False, backref="proxies")

    def __repr__(self):
        return f'{self.id} {self.ip_address}:{self.port}'


class Net_Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(BigInteger, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(String(length=100), nullable=False, unique=True)
    abbreviation = db.Column(String(length=10), nullable=False, unique=True, index=True)
    resource_type = db.Column(String(length=100), nullable=False)
    valid_accounts = db.relationship("Account", backref="resources", lazy=True)

    def __repr__(self):
        return f'{self.id} {self.name}'


class Lock(db.Model):
    __tablename__ = 'locks'

    id = db.Column(BigInteger, primary_key=True,
                   autoincrement=True, nullable=False)
    locked_account = db.Column(BigInteger, db.ForeignKey("accounts.id"), nullable=True)
    locked_proxy = db.Column(BigInteger, db.ForeignKey("proxies.id"), nullable=True)
    locked_at = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = db.Column(DateTime)

    def __repr__(self):
        return f'{self.id} {self.name}'
