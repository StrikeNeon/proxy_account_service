from datetime import datetime
from flask import request
from flask_restful import Resource
from . import db
from .schema import (account_schema, accounts_schema,
                     lock_schema, locks_schema,
                     proxy_schema, proxies_schema,
                     resource_schema, resources_schema)
from .models import Account, Lock, Proxy, Net_Resource


class Init_page(Resource):

    def get(self):
        return {'docs_data': 'fields'}


class Account_maker(Resource):

    def post(self):
        new_account = Account(
            login=request.json.get('login'),
            password=request.json.get('password'),
            resource=request.json.get('resource'),
            api_key=request.json.get('api_key'),
            email=request.json.get('email'),
            phone=request.json.get('phone'),
            name=request.json.get('name'),
        )
        db.session.add(new_account)
        db.session.commit()
        return account_schema.dump(new_account)


class All_accounts(Resource):

    def get(self):
        accounts = Account.query.all()
        return accounts_schema.dump(accounts)


class Account_ops(Resource):

    def get(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        return account_schema.dump(account)

    def put(self, account_id):
        queried_account = Account.query.filter_by(id=account_id)
        queried_account.update({
                "login": request.json.get('login'),
                "password": request.json.get('password'),
                "resource": request.json.get('resource'),
                "api_key": request.json.get('api_key'),
                "email": request.json.get('email'),
                "phone": request.json.get('phone'),
                "name": request.json.get('name'),
            })
        db.session.commit()

    def patch(self, account_id):
        action = request.args.get('action')
        if action == "lock":
            if request.json.get("expires_at", None):
                new_lock = Lock(
                        locked_account=request.json.get('account_id'),
                        locked_at=datetime.now(),
                        expires_at=request.json.get('expires_at')
                    )
                db.session.add(new_lock)
                db.session.commit()
                return account_schema.dump(new_lock)
            else:
                return {"error": "Neither proxy id nor account id were provided"}
        elif action == "unlock":
            deleted_lock = Lock.query.filter_by(locked_account=account_id)
            deleted_lock.delete()
            db.session.commit()
            return account_schema.dump(deleted_lock)

    def delete_account(account_id):
        deleted_account = Account.query.filter_by(id=account_id)
        deleted_account.delete()
        db.session.commit()
        return account_schema.dump(deleted_account)


class Proxy_maker(Resource):

    def post(self):
        new_proxy = Proxy(
            ip_address=request.json.get('ip_address'),
            port=request.json.get('port'),
            username=request.json.get('username'),
            password=request.json.get('password'),
            ip_version=request.json.get('ip_version'),
            expires_at=request.json.get('expires_at'),
            valid_resources=request.json.get('valid_resources'),
        )
        db.session.add(new_proxy)
        db.session.commit()
        return account_schema.dump(new_proxy)


class All_proxies(Resource):

    def get(self):
        proxies = Proxy.query.all()
        return proxies_schema.dump(proxies)


class Proxy_ops(Resource):

    def get(self, proxy_id):
        proxy = Proxy.query.filter_by(id=proxy_id).first()
        return proxy_schema.dump(proxy)

    def put(self, proxy_id):
        queried_proxy = Proxy.query.filter_by(id=proxy_id)
        queried_proxy.update({
                "login": request.json.get('login'),
                "password": request.json.get('password'),
                "resource": request.json.get('resource'),
                "api_key": request.json.get('api_key'),
                "email": request.json.get('email'),
                "phone": request.json.get('phone'),
                "name": request.json.get('name'),
            })
        db.session.commit()

    def patch(self, proxy_id):
        action = request.args.get('action')
        if action == "lock":
            if request.json.get("expires_at", None):
                new_lock = Lock(
                        locked_proxy=proxy_id,
                        locked_at=datetime.now(),
                        expires_at=request.json.get('expires_at')
                    )
                db.session.add(new_lock)
                db.session.commit()
                return account_schema.dump(new_lock)
            else:
                return {"error": "Neither proxy id nor account id were provided"}
        elif action == "unlock":
            deleted_lock = Lock.query.filter_by(locked_proxy=proxy_id)
            deleted_lock.delete()
            db.session.commit()
            return account_schema.dump(deleted_lock)

    def delete_account(proxy_id):
        deleted_account = Proxy.query.filter_by(id=proxy_id)
        deleted_account.delete()
        db.session.commit()
        return account_schema.dump(deleted_account)


class Resorce_ops(Resource):

    def get(self, resource_id):
        return {'resource_data': 'fields'}

    def post(self, resource_id):
        return {'added_data': 'fields'}

    def put(self, resource_id):
        return {'changed_data': 'fields'}

    def delete(self, resource_id):
        return {'deleted_data': 'fields'}


class Lock_ops(Resource):

    def get(self, lock_id):
        account = Lock.query.filter_by(id=lock_id).first()
        if account:
            return lock_schema.dump(account)

    def post(self, lock_id):
        if request.json.get("expires_at", None):
            if request.json.get("locked_account") or request.json.get("locked_proxy"):
                new_lock = Lock(
                        locked_account=request.json.get('account_id', None),
                        locked_proxy=request.json.get('proxy_id', None),
                        locked_at=datetime.now(),
                        expires_at=request.json['expires_at']
                    )
                db.session.add(new_lock)
                db.session.commit()
                return account_schema.dump(new_lock)
            else:
                return {"error": "Neither proxy id nor account id were provided"}
        else:
            return {"error": "Expiry datetime was not provided"}

    def put(self, lock_id):
        return {'changed_data': 'fields'}

    def delete(self, lock_id):
        return {'unlocked_proxy': 'fields',
                'unlocked_account': 'fields'}
