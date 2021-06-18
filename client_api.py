import requests
import json


class PAS_client():

    def __init__(self, address: str = "127.0.0.1", port: int = 5000):
        self.address = address
        self.port = port

    def get_all_accounts(self):
        responce = requests.get(f"http://{self.address}:{self.port}/api/accounts")
        if responce.status_code == 200:
            return responce.json()

    def get_account_by_id(self, account_id):
        responce = requests.get(f"http://{self.address}:{self.port}/api/account/{account_id}")
        if responce.status_code == 200:
            return responce.json()

    def add_account(self, account_dict):
        headers = {"content-type": "application/json"}
        responce = requests.post(f"http://{self.address}:{self.port}/api/add_account",headers=headers, data=json.dumps(account_dict))
        if responce.status_code == 200:
            return responce.json()

    def get_all_proxies(self):
        responce = requests.get(f"http://{self.address}:{self.port}/api/proxies")
        if responce.status_code == 200:
            return responce.json()

    def get_proxy_by_id(self, proxy_id):
        responce = requests.get(f"http://{self.address}:{self.port}/api/proxy/{proxy_id}")
        if responce.status_code == 200:
            return responce.json()

    def add_proxy(self, proxy_dict):
        headers = {"content-type": "application/json"}
        responce = requests.post(f"http://{self.address}:{self.port}/api/add_proxy",headers=headers, data=json.dumps(proxy_dict))
        if responce.status_code == 200:
            return responce.json()

    def get_all_locks(self):
        responce = requests.get(f"http://{self.address}:{self.port}/api/locks")
        if responce.status_code == 200:
            return responce.json()

    def get_all_resources(self):
        responce = requests.get(f"http://{self.address}:{self.port}/api/resources")
        if responce.status_code == 200:
            return responce.json()

    def get_resource_by_id(self, resource_id):
        responce = requests.get(f"http://{self.address}:{self.port}/api/resource/{resource_id}")
        if responce.status_code == 200:
            return responce.json()

    def add_resource(self, resource_dict):
        headers = {"content-type": "application/json"}
        responce = requests.post(f"http://{self.address}:{self.port}/api/add_resource",headers=headers, data=json.dumps(resource_dict))
        if responce.status_code == 200:
            return responce.json()


if __name__ == "__main__":

    pas = PAS_client()
    accounts = pas.get_all_accounts()
    print(accounts)

    resources = pas.get_all_resources()
    print(resources)

    resource = pas.get_resource_by_id(1)
    print(resource)

    account = pas.get_account_by_id(1)
    print(account)

    # new_resource = pas.add_resource({"name": "vkontakte", "abbreviation": "vk", "resource_type": "social network"})
    # print(new_resource)

    # new_account = pas.add_account({"login": "test_login",
    #                            "password": "test_password",
    #                            "resource": 1, "api_key": None,
    #                            "email": None, "phone": None,
    #                            "name": "fake name"})
    # print(new_account)

    # new_proxy = pas.add_proxy({"ip_address": "127.0.0.1",
    #                          "port": 5885,
    #                          "username": "name", "password": "password",
    #                          "ip_version": "ipv6", "renewed_at": None,
    #                          "expires_at": "fake name"}, 
    #                          "valid_resources": {"valid_for":["vk"]}},
    # print(new_proxy)