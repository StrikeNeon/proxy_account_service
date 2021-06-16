import psycopg2


def get_proxy(data):
    return {'proxy_data': 'fields'}


def add_proxy(data):
    return {'added_data': 'fields'}


def update_proxy(data):
    return {'changed_data': 'fields'}


def lock_proxy(data):
    return {'lock_data': 'fields'}


def unlock_proxy(data):
    return {'lock_remove_data': 'fields'}


def delete_proxy(data):
    return {'deleted_data': 'fields'}
