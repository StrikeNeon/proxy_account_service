from datetime import datetime
from sqlalchemy import exc as sql_exceptions
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
        account_login = request.json.get('login', None)
        account_password = request.json.get('password', None)
        resource = request.json.get('resource', None)
        if account_login and account_password and resource:
            new_account = Account(
                login=account_login,
                password=account_password,
                resource=resource,
                api_key=request.json.get('api_key'),
                email=request.json.get('email'),
                phone=request.json.get('phone'),
                name=request.json.get('name'),
            )
            db.session.add(new_account)
            db.session.commit()
            return account_schema.dump(new_account)
        else:
            return {"error": "one or more non nullable fields was not supplied"}, 400, {'content-type': 'application/json'}


class Multiple_account_ops(Resource):

    def get(self):
        filter_type = request.args.get('filter', None)
        if not filter_type:
            accounts = Account.query.all()
            return accounts_schema.dump(accounts)

    def patch(self):
        accounts = request.json.get('accounts', None)
        if not accounts or type(accounts) != list:
            return {"error": "account ids were not supplied or key malformed"}
        action = request.args.get('action')
        if action == "lock":
            locked_accounts = []
            for account_id in accounts:
                if account_id.get("expires_at", None):
                    new_lock = Lock(
                            locked_account=account_id.get('account_id'),
                            locked_at=datetime.now(),
                            expires_at=account_id.get('expires_at')
                        )
                    db.session.add(new_lock)
                    db.session.commit()
                    locked_accounts.append(new_lock)
                else:
                    print({"error": "No expiry provided",
                           "account": account_id})
            return {"locked_accounts": locks_schema.dump(locked_accounts)}
        elif action == "unlock":
            locked_accounts = []
            for account_id in accounts:
                deleted_lock = Lock.query.filter_by(locked_account=account_id.get('account_id'))
                deleted_lock.delete()
                db.session.commit()
                locked_accounts.append(new_lock)
            return {"unlocked_accounts": locks_schema.dump(locked_accounts)}
        else:
            return {"error": "action missing or unknown"}

    def delete_account(self):
        accounts = request.json.get('accounts', None)
        if not accounts or type(accounts) != list:
            return {"error": "account ids were not supplied or key malformed"}
        deleted_accounts = []
        for account_id in accounts:
            deleted_account = Account.query.filter_by(id=account_id.get('id'))
            deleted_account.delete()
            db.session.commit()
            deleted_accounts.append(deleted_account)
        return {"deleted_accounts": accounts_schema.dump(deleted_accounts)}


class Account_ops(Resource):

    def get(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        return account_schema.dump(account)

    def put(self, account_id):
        table_columns = [col.name for col in Account.__table__.columns]  # get model column names
        update_dict = {key: value for key, value
                       in request.json.items() if key in table_columns}  # parse request json to only get necessary data
        queried_account = Account.query.filter_by(id=account_id)
        queried_account.update(update_dict)
        db.session.commit()
        return account_schema.dump(queried_account)

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
                return lock_schema.dump(new_lock)
            else:
                return {"error": "No expiry provided"}, 400, {'content-type': 'application/json'}
        elif action == "unlock":
            deleted_lock = Lock.query.filter_by(locked_account=account_id)
            deleted_lock.delete()
            db.session.commit()
            return lock_schema.dump(deleted_lock)

    def delete_account(account_id):
        deleted_account = Account.query.filter_by(id=account_id)
        deleted_account.delete()
        db.session.commit()
        return account_schema.dump(deleted_account)


class Proxy_maker(Resource):

    def post(self):
        ip_address = request.json.get('ip_address', None)
        port = request.json.get('port', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        ip_version = request.json.get('ip_version', None)
        renewed_at = datetime.fromtimestamp(request.json.get('renewed_at', None))
        expires_at = datetime.fromtimestamp(request.json.get('expires_at', None))
        valid_resources = request.json.get('valid_resources', None)
        if ip_address and port and username and password and ip_version and renewed_at and expires_at and valid_resources:
            new_proxy = Proxy(
                ip_address=ip_address,
                port=port,
                username=username,
                password=password,
                ip_version=ip_version,
                renewed_at=renewed_at,
                expires_at=expires_at,
                valid_resources=valid_resources,
            )
            db.session.add(new_proxy)
            db.session.commit()
            return proxy_schema.dump(new_proxy)
        else:
            return {"error": "one or more non nullable fields was not supplied"}, 400, {'content-type': 'application/json'}


class Multiple_proxy_ops(Resource):

    def get(self):
        filter_type = request.args.get('filter', None)
        if not filter_type:
            proxies = Proxy.query.all()
            return proxies_schema.dump(proxies)

    def patch(self):
        proxies = request.json.get('proxies', None)
        if not proxies or type(proxies) != list:
            return {"error": "proxy ids were not supplied or key malformed"}
        action = request.args.get('action')
        if action == "lock":
            locked_proxies = []
            for proxy_id in proxies:
                if proxy_id.get("expires_at", None):
                    new_lock = Lock(
                            locked_proxy=proxy_id.get('proxy_id'),
                            locked_at=datetime.now(),
                            expires_at=proxy_id.get('expires_at')
                        )
                    db.session.add(new_lock)
                    db.session.commit()
                    locked_proxies.append(new_lock)
                else:
                    print({"error": "No expiry provided",
                           "proxy": proxy_id})
            return {"locked_proxies": locks_schema.dump(locked_proxies)}
        elif action == "unlock":
            locked_proxies = []
            for proxy_id in proxies:
                deleted_lock = Lock.query.filter_by(locked_proxy=proxy_id.get('proxy_id'))
                deleted_lock.delete()
                db.session.commit()
                locked_proxies.append(new_lock)
            return {"unlocked_proxies": locks_schema.dump(locked_proxies)}
        else:
            return {"error": "action missing or unknown"}, 400, {'content-type': 'application/json'}

    def delete_account(self):
        proxies = request.json.get('accounts', None)
        if not proxies or type(proxies) != list:
            return {"error": "proxy ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        deleted_proxies = []
        for proxy_id in proxies:
            deleted_proxy = Proxy.query.filter_by(id=proxy_id.get('id'))
            deleted_proxy.delete()
            db.session.commit()
            deleted_proxies.append(deleted_proxy)
        return {"deleted_proxies": accounts_schema.dump(deleted_proxies)}


class Proxy_ops(Resource):

    def get(self, proxy_id):
        proxy = Proxy.query.filter_by(id=proxy_id).first()
        return proxy_schema.dump(proxy)

    def put(self, proxy_id):
        table_columns = [col.name for col in Proxy.__table__.columns]
        update_dict = {key: value for key, value
                       in request.json.items() if key in table_columns}
        queried_proxy = Proxy.query.filter_by(id=proxy_id)
        queried_proxy.update(update_dict)
        db.session.commit()
        return proxy_schema.dump(queried_proxy)

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
                return lock_schema.dump(new_lock)
            else:
                return {"error": "No expiry provided"}
        elif action == "unlock":
            deleted_lock = Lock.query.filter_by(locked_proxy=proxy_id)
            deleted_lock.delete()
            db.session.commit()
            return lock_schema.dump(deleted_lock)

    def delete_account(proxy_id):
        deleted_proxy = Proxy.query.filter_by(id=proxy_id)
        deleted_proxy.delete()
        db.session.commit()
        return proxy_schema.dump(deleted_proxy)


class Multiple_resource_ops(Resource):

    def get(self):
        filter_type = request.args.get('filter', None)
        if not filter_type:
            resources = Net_Resource.query.all()
            return resources_schema.dump(resources)


class Resource_maker(Resource):

    def post(self):
        # TODO this could be used for a unified approach, also to avoid assinging nulls in put reqests
        # non_nullable = [col.name for col in Net_Resource.__table__.columns if not col.nullable]
        # additional = [col.name for col in Net_Resource.__table__.columns if col.nullable]
        # print(non_nullable, additional)
        resource_name = request.json.get('name', None)
        resource_abbrev = request.json.get('abbreviation', None)
        resource_type = request.json.get('resource_type', None)
        if resource_name and resource_abbrev and resource_type:
            try:
                new_resource = Net_Resource(
                    name=resource_name,
                    abbreviation=resource_abbrev,
                    resource_type=resource_type
                )
                db.session.add(new_resource)
                db.session.commit()
                return resource_schema.dump(new_resource)
            except sql_exceptions.IntegrityError:
                return {"error": "this resource is already registered"}, 400, {'content-type': 'application/json'}
        else:
            return {"error": "one or more non nullable fields was not supplied"}, 400, {'content-type': 'application/json'}


class Resorce_ops(Resource):

    def get(self, resource_id):
        resource = Net_Resource.query.filter_by(id=resource_id).first()
        return resource_schema.dump(resource)

    def put(self, resource_id):
        table_columns = [col.name for col in Net_Resource.__table__.columns]
        update_dict = {key: value for key, value
                       in request.json.items() if key in table_columns}
        queried_resource = Net_Resource.query.filter_by(id=resource_id)
        queried_resource.update(update_dict)
        db.session.commit()
        return resource_schema.dump(new_resource)

    def delete(self, resource_id):
        deleted_resource = Net_Resource.query.filter_by(id=resource_id)
        deleted_resource.delete()
        db.session.commit()
        return resource_schema.dump(deleted_resource)


class Interlock(Resource):

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
                return lock_schema.dump(new_lock)
            else:
                return {"error": "Neither proxy id nor account id were provided"}
        else:
            return {"error": "Expiry datetime was not provided"}


class Lock_ops(Resource):

    def get(self, lock_id):
        account = Lock.query.filter_by(id=lock_id).first()
        if account:
            return lock_schema.dump(account)

    def put(self, lock_id):
        table_columns = [col.name for col in Lock.__table__.columns]
        update_dict = {key: value for key, value
                       in request.json.items() if key in table_columns}
        queried_lock = Lock.query.filter_by(id=lock_id)
        queried_lock.update(update_dict)
        db.session.commit()
        return lock_schema.dump(queried_lock)

    def delete(self, lock_id):
        deleted_lock = Lock.query.filter_by(id=lock_id)
        deleted_lock.delete()
        db.session.commit()
        return lock_schema.dump(deleted_lock)
