from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from .router import add_routes

app = Flask(__name__)
app.config.from_object('proxy_account_service.settings')

db = SQLAlchemy(app)
migrate = Migrate()
mallow = Marshmallow(app)

db.init_app(app)
migrate.init_app(app, db)

api = Api(app)
add_routes(api)

import proxy_account_service.models
