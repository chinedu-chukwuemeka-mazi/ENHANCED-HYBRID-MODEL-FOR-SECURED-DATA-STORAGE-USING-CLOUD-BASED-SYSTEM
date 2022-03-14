from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(APP_ROOT, 'static/')

app = Flask(__name__)
app.config['DATABASE_DIR'] = DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(DB, 'db/hybrid.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Mr\x0b@3\x94\x88\x8ey\x1a\x140\x9dr_\xd8x\xff\xd7\xfe\xc6~_\x9e'

#define database object
db = SQLAlchemy(app)

#define migrate object
migrate = Migrate(app, db)

#import routes from app
from app import routes
