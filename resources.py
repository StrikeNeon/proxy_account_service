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


class general_request_processor():

    def __init__(self, model, schema, request_json):
        self.model = model
        self.schema = schema
        self.json_data = request_json

    def make_record(self):
        # this isn't the best way here, can't think of anything else
        non_nullable = [col.name for col in self.model.__table__.columns if not col.nullable and col.name != "id"]
        if len(non_nullable) == len([key for key in self.json_data.keys() if key in non_nullable]):
            additional = [col.name for col in self.model.__table__.columns if col.nullable]
            record_dict = {key: value for key, value
                           in self.json_data.items()
                           if key in non_nullable or additional}
            if record_dict.get("renewed_at", None):
                record_dict["renewed_at"] = datetime.fromtimestamp(self.json_data.get('renewed_at'))
            if record_dict.get("expires_at", None):
                record_dict["expires_at"] = datetime.fromtimestamp(self.json_data.get('expires_at'))
            try:
                new_record = self.model(**record_dict)
                db.session.add(new_record)
                db.session.commit()
                return self.schema.dump(new_record)
            except sql_exceptions.IntegrityError:
                return {"error": "this record is already registered"}, 400, {'content-type': 'application/json'}
        else:
            return {"error": "one or more non nullable fields was not supplied"}, 400, {'content-type': 'application/json'}

    def update_record(self, record_id: str):
        table_columns = [col.name for col in self.model.__table__.columns]  # get model column names
        update_dict = {key: value for key, value
                       in self.json_data.items() if key in table_columns}  # parse request json to only get necessary data
        queried_record = self.model.query.filter_by(id=record_id)
        queried_record.update(update_dict)
        db.session.commit()
        return self.schema.dump(queried_record)

    def make_lock(self, requested_id: str, many: bool = False):
        if request.json.get("expires_at", None):
            if self.model == Account:
                check_lock = Lock.query.filter_by(locked_account=requested_id)
                if len(check_lock) > 0:
                    if many:
                        return check_lock
                    return {"error": f"account {requested_id} already locked"}, 201, {'content-type': 'application/json'}
                new_lock = Lock(
                            locked_account=self.json_data.get(requested_id),
                            locked_at=datetime.now(),
                            expires_at=datetime.fromtimestamp(self.json_data.get('expires_at'))
                            )
                db.session.add(new_lock)
                db.session.commit()
                if many:
                    return new_lock
                return lock_schema.dump(new_lock)
            else:
                check_lock = Lock.query.filter_by(locked_proxy=requested_id)
                if len(check_lock) > 0:
                    if many:
                        return check_lock
                    return {"error": f"proxy {requested_id} already locked at {check_lock.id}"}, 201, {'content-type': 'application/json'}
                new_lock = Lock(locked_proxy=self.json_data.get(requested_id),
                                locked_at=datetime.now(),
                                expires_at=datetime.fromtimestamp(self.json_data.get('expires_at'))
                                )
                db.session.add(new_lock)
                db.session.commit()
                if many:
                    return new_lock
                return lock_schema.dump(new_lock)
        else:
            return {"error": "No expiry provided"}, 400, {'content-type': 'application/json'}

    def unmake_lock(self, requested_id: str, many: bool = False):
        if self.model == Account:
            deleted_lock = Lock.query.filter_by(locked_account=requested_id)
        else:
            deleted_lock = Lock.query.filter_by(locked_proxy=requested_id)
        if deleted_lock:
            deleted_lock.delete()
            db.session.commit()
            if many:
                return deleted_lock
            return lock_schema.dump(deleted_lock)
        else:
            if many:
                return
            return {"error": "wasn't locked"}, 201, {'content-type': 'application/json'}


class Init_page(Resource):

    def get(self):
        return {'docs_data': 'fields'}


class Account_maker(Resource):

    def post(self):
        maker = general_request_processor(Account, account_schema, request.json)
        new_account = maker.make_record()
        return new_account


class Multiple_account_ops(Resource):

    def get(self):
        filter_type = request.args.get('filter', None)
        if not filter_type:
            accounts = Account.query.all()
            return accounts_schema.dump(accounts)

    def patch(self):
        accounts = request.json.get('accounts', None)
        if not accounts or type(accounts) != list:
            return {"error": "account ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        action = request.args.get('action')
        if action == "lock":
            locked_accounts = []
            for account_id in accounts:
                maker = general_request_processor(Account, account_schema, account_id)
                new_lock = maker.make_lock(account_id.get('account_id'), many=True)
                if new_lock:
                    locked_accounts.append(new_lock)
            return {"locked_accounts": locks_schema.dump(locked_accounts)}
        elif action == "unlock":
            unlocked_accounts = []
            for account_id in accounts:
                maker = general_request_processor(Account, account_schema, account_id)
                deleted_lock_lock = maker.unmake_lock(account_id.get('account_id'), many=True)
                if new_lock:
                    unlocked_accounts.append(deleted_lock_lock)
            return {"unlocked_accounts": locks_schema.dump(unlocked_accounts)}
        else:
            return {"error": "action missing or unknown"}, 400, {'content-type': 'application/json'}

    def delete(self):
        accounts = request.args.get('accounts', None)
        accounts = accounts.split(",")
        if not accounts or type(accounts) != list:
            return {"error": "account ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        deleted_accounts = []
        for account_id in accounts:
            deleted_account = Account.query.filter_by(id=account_id)
            deleted_account.delete()
            db.session.commit()
            deleted_accounts.append(deleted_account)
        return {"deleted_accounts": accounts_schema.dump(deleted_accounts)}


class Account_ops(Resource):

    def get(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        return account_schema.dump(account)

    def put(self, account_id):
        updater = general_request_processor(Account, account_schema, request.json)
        updated_record = updater.update_record(account_id)
        return updated_record

    def patch(self, account_id):
        locker = general_request_processor(Account, account_schema, request.json)
        action = request.args.get('action')
        if action == "lock":
            new_lock = locker.make_lock(account_id)
        return new_lock

    def delete(self, account_id):
        deleted_account = Account.query.filter_by(id=account_id)
        deleted_account.delete()
        db.session.commit()
        return account_schema.dump(deleted_account)


class Proxy_maker(Resource):

    def post(self):
        maker = general_request_processor(Proxy, proxy_schema, request.json)
        new_proxy = maker.make_record()
        return new_proxy


class Multiple_proxy_ops(Resource):

    def get(self):
        filter_type = request.args.get('filter', None)
        if not filter_type:
            proxies = Proxy.query.all()
            return proxies_schema.dump(proxies)

    def patch(self):
        proxies = request.json.get('proxies', None)
        if not proxies or type(proxies) != list:
            return {"error": "account ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        action = request.args.get('action')
        if action == "lock":
            locked_proxies = []
            for proxy_id in proxies:
                maker = general_request_processor(Proxy, proxy_schema, proxy_id)
                new_lock = maker.make_lock(proxy_id.get('proxy_id'), many=True)
                if new_lock:
                    locked_proxies.append(new_lock)
            return {"locked_proxies": locks_schema.dump(locked_proxies)}
        elif action == "unlock":
            unlocked_proxies = []
            for proxy_id in proxies:
                maker = general_request_processor(Proxy, proxy_schema, proxy_id)
                deleted_lock_lock = maker.unmake_lock(proxy_id.get('proxy_id'), many=True)
                if new_lock:
                    unlocked_proxies.append(deleted_lock_lock)
            return {"unlocked_proxies": locks_schema.dump(unlocked_proxies)}
        else:
            return {"error": "action missing or unknown"}, 400, {'content-type': 'application/json'}

    def delete(self):
        proxies = request.args.get('proxies', None)
        proxies = proxies.split(",")
        if not proxies or type(proxies) != list:
            return {"error": "proxy ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        deleted_proxies = []
        for proxy_id in proxies:
            deleted_proxy = Proxy.query.filter_by(id=proxy_id)
            deleted_proxy.delete()
            db.session.commit()
            deleted_proxies.append(deleted_proxy)
        return {"deleted_proxies": accounts_schema.dump(deleted_proxies)}


class Proxy_ops(Resource):

    def get(self, proxy_id):
        proxy = Proxy.query.filter_by(id=proxy_id).first()
        return proxy_schema.dump(proxy)

    def put(self, proxy_id):
        updater = general_request_processor(Proxy, proxy_schema, request.json)
        updated_record = updater.update_record(proxy_id)
        return updated_record

    def patch(self, proxy_id):
        locker = general_request_processor(Proxy, proxy_schema, request.json)
        new_lock = locker.make_lock(proxy_id, request.args)
        return new_lock

    def delete(self, proxy_id):
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

    def delete(self):
        resources = request.args.get('resources', None)
        resources = resources.split(",")
        if not resources or type(resources) != list:
            return {"error": "proxy ids were not supplied or key malformed"}, 400, {'content-type': 'application/json'}
        deleted_resources = []
        for resource_id in resources:
            deleted_resource = Net_Resource.query.filter_by(id=resource_id)
            deleted_resource.delete()
            db.session.commit()
            deleted_resources.append(deleted_resource)
        return {"deleted_proxies": resources_schema.dump(deleted_resources)}


class Resource_maker(Resource):

    def post(self):
        maker = general_request_processor(Net_Resource, resource_schema, request.json)
        new_resource = maker.make_record()
        return new_resource


class Resorce_ops(Resource):

    def get(self, resource_id):
        resource = Net_Resource.query.filter_by(id=resource_id).first()
        return resource_schema.dump(resource)

    def delete(self, resource_id):
        deleted_resource = Net_Resource.query.filter_by(id=resource_id)
        deleted_resource.delete()
        db.session.commit()
        return resource_schema.dump(deleted_resource)


class Interlock(Resource):

    def post(self):
        json_data = request.json
        json_data["locked_at"] = datetime.now()
        maker = general_request_processor(Lock, lock_schema, request.json)
        new_lock = maker.make_record()
        return new_lock


class Lock_ops(Resource):

    def get(self, lock_id):
        account = Lock.query.filter_by(id=lock_id).first()
        if account:
            return lock_schema.dump(account)

    def put(self, lock_id):
        updater = general_request_processor(Lock, lock_schema, request.json)
        updated_record = updater.update_record(lock_id)
        return updated_record

    def delete(self, lock_id):
        deleted_lock = Lock.query.filter_by(id=lock_id)
        deleted_lock.delete()
        db.session.commit()
        return lock_schema.dump(deleted_lock)
