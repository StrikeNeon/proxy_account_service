from flask import request
from flask_restful import Resource
from .Account_functions import (get_account,
                                add_account,
                                update_account,
                                delete_account)

from .Proxy_functions import (get_proxy,
                              add_proxy,
                              update_proxy,
                              delete_proxy)

from .Lock_functions import (get_lock,
                             make_lock,
                             update_lock,
                             delete_lock)

from .Resource_functions import (get_resource,
                                 post_resource,
                                 update_resource,
                                 delete_resource)


class Init_page(Resource):

    def get(self):
        return {'docs_data': 'fields'}


class Account_ops(Resource):

    def get(self, account_id):
        return get_account(account_id)

    def post(self, account_id):
        data = request.form['data']
        return add_account(data)

    def put(self, account_id):
        data = request.form['data']
        return update_account(data)

    # def patch(self):
    #     param = "lock"
    #     return lock_account() if param == "lock" else unlock_account()

    def delete(self, account_id):
        return delete_account(account_id)


class Proxy_ops(Resource):

    def get(self, proxy_id):
        return get_proxy(proxy_id)

    def post(self, proxy_id):
        data = request.form['data']
        return add_proxy(data)

    def put(self, proxy_id):
        data = request.form['data']
        return update_proxy(data)

    # def patch(self):
    #     param = "lock"
    #     return lock_proxy() if param == "lock" else unlock_proxy()

    def delete(self, proxy_id):
        return delete_proxy(proxy_id)


class Resorce_ops(Resource):

    def get(self, resource_id):
        return get_resource(resource_id)

    def post(self, resource_id):
        data = request.form['data']
        return post_resource(data)

    def put(self, resource_id):
        data = request.form['data']
        return update_resource(data)

    def delete(self, resource_id):
        return delete_resource(resource_id)


class Lock_ops(Resource):

    def get(self, lock_id):
        return get_lock(lock_id)

    def post(self, lock_id):
        data = request.form['data']
        return make_lock(data)

    def put(self, lock_id):
        data = request.form['data']
        return update_lock(data)

    def delete(self, lock_id):
        return delete_lock(lock_id)
