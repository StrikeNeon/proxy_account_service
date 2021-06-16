from flask import request
from . import db
from .schema import account_schema, accounts_schema
from .models import Account


def get_account(account_id):
    account = Account.query.filter_by(id=account_id).first()
    return account_schema.dump(account)


def get_accounts():
    accounts = Account.query.all()
    return accounts_schema.dump(accounts)


def add_account():
    new_account = Account(
            login=request.json['login'],
            password=request.json['password'],
            resource=request.json['resource'],
            api_key=request.json['api_key'],
            email=request.json['email'],
            phone=request.json['phone'],
            name=request.json['name'],
        )
    db.session.add(new_account)
    db.session.commit()
    return account_schema.dump(new_account)


def update_account(data):
    return {'changed_data': 'fields'}


def lock_account(data):
    return {'lock_data': 'fields'}


def unlock_account(data):
    return {'lock_remove_data': 'fields'}


def delete_account(data):
    return {'deleted_data': 'fields'}
