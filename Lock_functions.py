import psycopg2


def get_lock(data):
    return {'lock_data': 'fields'}


def make_lock(data):
    return {'locked_proxy': 'fields',
            'locked_account': 'fields'}


def update_lock(data):
    return {'changed_data': 'fields'}


def delete_lock(data):
    return {'unlocked_proxy': 'fields',
            'unlocked_account': 'fields'}
