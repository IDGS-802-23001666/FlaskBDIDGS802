from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect()

@app.route("/", methods = ['GET', 'POST'])
@app.route("/index")
def index():
	create_form = forms.UserForm(request.form)
	alumno = Alumnos.query.all()
	return render_template("index.html", form = create_form, alumno = alumno)


@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        alumn = Alumnos(
            nombre=create_form.nombre.data,
            aPaterno=create_form.aPaterno.data,
            email=create_form.email.data
        )
        db.session.add(alumn)
        db.session.commit()     
        return redirect(url_for('index'))
    
    return render_template("Alumnos.html", form=create_form)


@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    # Inicializamos la variable como None por seguridad
    alumn1 = None
    
    id = request.args.get('id')
    if id:
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    
    if not alumn1:
        return redirect(url_for('index'))
        
    return render_template("detalles.html", alumn=alumn1)


@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id = request.args.get('id')
        create_form.nombre = alumn1.nombre
        create_form.aPaterno = alumn1.aPaterno
        create_form.email = alumn1.email
    if request.method=='POST0':
         id = create_form.id.data
         alumn1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
         alumn1.id=id
         alumn1.nombre=str.rstrip(create_form.nombre.data)
         alumn1.aPaterno=create_form.aPaterno.data
         db.session.add(alumn1)
         db.session.commit()
         return redirect(url_for('index'))
    return render_template("modificar.html", nombre = nombre, aPaterno = aPaterno, email = email)



@app.errorhandler(404)
def error(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
