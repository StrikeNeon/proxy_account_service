from . import app
from flask_restful import Api
from .router import add_routes

api = Api(app)
add_routes(api)
app.run(debug=True)
