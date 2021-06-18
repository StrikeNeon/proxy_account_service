from .resources import (Init_page,
                        Account_maker,
                        Multiple_account_ops,
                        Account_ops,
                        Proxy_maker,
                        Multiple_proxy_ops,
                        Proxy_ops,
                        Resource_maker,
                        Multiple_resource_ops,
                        Resorce_ops,
                        Interlock,
                        Lock_ops)


def add_routes(api):
    api.add_resource(Init_page, '/api')
    api.add_resource(Account_maker, '/api/add_account')
    api.add_resource(Multiple_account_ops, '/api/accounts')
    api.add_resource(Account_ops, '/api/account/<string:account_id>')
    api.add_resource(Proxy_maker, '/api/add_proxy')
    api.add_resource(Multiple_proxy_ops, '/api/proxies')
    api.add_resource(Proxy_ops, '/api/proxy/<string:proxy_id>')
    api.add_resource(Resource_maker, '/api/add_resource')
    api.add_resource(Multiple_resource_ops, '/api/resources')
    api.add_resource(Resorce_ops, '/api/resource/<string:resource_id>')
    api.add_resource(Interlock, '/api/interlock')
    api.add_resource(Lock_ops, '/api/lock/<string:lock_id>')
