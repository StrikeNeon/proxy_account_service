from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object('PAS_app.settings')

db = SQLAlchemy(app)
migrate = Migrate()
mallow = Marshmallow(app)

db.init_app(app)
migrate.init_app(app, db)

import PAS_app.models
