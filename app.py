from . import app
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from .router import add_routes

api = Api(app)
add_routes(api)


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Proxy Account Service"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


app.run(debug=True)
