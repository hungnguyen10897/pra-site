from flask import Flask, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pra:pra@localhost/pra2'
db = SQLAlchemy(app)

from pra_site import routes