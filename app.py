from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect()

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")


@app.route("/alumnos")
def alumnos():
	return render_template("Alumnos.html")

@app.errorhandler(404)
def error(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
