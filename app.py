from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db
from maestros.routes import maestros_bp
from alumnos.routes import alumnos_bp 
from cursos.routes import cursos_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)

db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)

@app.route("/")
def index_general():
    return render_template("indexIndex.html")

@app.errorhandler(404)
def error(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()