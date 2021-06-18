import requests
import json


def get_all_accounts():
    responce = requests.get("http://127.0.0.1:5000/api/accounts")
    if responce.status_code == 200:
        return responce.json()

def add_account(account_dict):
    headers = {"content-type": "application/json"}
    responce = requests.post("http://127.0.0.1:5000/api/add_account",headers=headers, data=json.dumps(account_dict))
    if responce.status_code == 200:
        return responce.json()

def get_all_proxies():
    responce = requests.get("http://127.0.0.1:5000/api/proxies")
    if responce.status_code == 200:
        return responce.json()

def get_all_locks():
    responce = requests.get("http://127.0.0.1:5000/api/locks")
    if responce.status_code == 200:
        return responce.json()

def get_all_resources():
    responce = requests.get("http://127.0.0.1:5000/api/resources")
    if responce.status_code == 200:
        return responce.json()

def get_resource_by_id(resource_id):
    responce = requests.get(f"http://127.0.0.1:5000/api/resource/{resource_id}")
    if responce.status_code == 200:
        return responce.json()

def add_resource(resource_dict):
    headers = {"content-type": "application/json"}
    responce = requests.post("http://127.0.0.1:5000/api/add_resource",headers=headers, data=json.dumps(resource_dict))
    if responce.status_code == 200:
        return responce.json()

accounts = get_all_accounts()
print(accounts)

resources = get_all_resources()
print(resources)

resource = get_resource_by_id(1)
print(resource)

# new_resource = add_resource({"name": "vkontakte", "abbreviation": "vk", "resource_type": "social network"})
# print(new_resource)

# new_account = add_account({"name": "vkontakte", "abbreviation": "vk", "resource_type": "social network"})
# print(new_resource)