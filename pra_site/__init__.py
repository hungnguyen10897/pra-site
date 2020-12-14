from flask import Flask, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json

with open("/etc/pra-site-config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = config["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = config["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)

from pra_site import routes