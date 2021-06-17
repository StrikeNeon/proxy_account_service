from .resources import (Init_page,
                        Account_maker,
                        All_accounts,
                        Account_ops,
                        Proxy_ops,
                        Resorce_ops,
                        Lock_ops)


def add_routes(api):
    api.add_resource(Init_page, '/api/')
    api.add_resource(Account_maker, '/api/add_account/')
    api.add_resource(All_accounts, '/api/get_all_accounts/')
    api.add_resource(Account_ops, '/api/account/<string:account_id>')
    api.add_resource(Proxy_ops, '/api/proxy/<string:proxy_id>')
    api.add_resource(Resorce_ops, '/api/resorce/<string:resource_id>')
    api.add_resource(Lock_ops, '/api/lock/<string:lock_id>')
