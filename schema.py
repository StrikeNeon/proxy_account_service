from . import mallow
from .models import Account, Proxy, Resource, Lock


class AccountSchema(mallow.Schema):
    class Meta:
        fields = ("id", "login", "password",
                  "resource", "api_key",
                  "email", "phone", "name")
        model = Account


class ProxySchema(mallow.Schema):
    class Meta:
        fields = ("id", "ip_address", "port",
                  "username", "password",
                  "ip_version", "renewed_at",
                  "expires_at", "valid_resources")
        model = Proxy


class ResourceSchema(mallow.Schema):
    class Meta:
        fields = ("id", "name",
                  "abbreviation",
                  "resource_type")
        model = Resource


class LockSchema(mallow.Schema):
    class Meta:
        fields = ("id", "locked_account",
                  "locked_proxy", "locked_at",
                  "expires_at")
        model = Lock


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

proxy_schema = ProxySchema()
proxies_schema = ProxySchema(many=True)

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

lock_schema = LockSchema()
lockss_schema = LockSchema(many=True)
