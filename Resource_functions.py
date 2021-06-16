import psycopg2


def get_resource(data):
    return {'resource_data': 'fields'}


def post_resource(data):
    return {'added_data': 'fields'}


def update_resource(data):
    return {'changed_data': 'fields'}


def delete_resource(data):
    return {'deleted_data': 'fields'}