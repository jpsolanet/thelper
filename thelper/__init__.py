from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from .config import Config

APP = Flask(__name__)

APP.config.from_object(Config)
DB = SQLAlchemy(APP)

MIGRATE = Migrate(APP, DB, render_as_batch=True)

# Import stuffs
from . import routes, models

from thelper.admin_views import admin_views

ADMIN = Admin(
    APP,
    name="thelper",
    template_mode="bootstrap3",
)
for name, view in admin_views.items():
    mv = view["type"](view["model"], DB.session, category=view["category"])
    ADMIN.add_view(mv)
