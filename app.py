from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from maestros.routes import maestros_bp
import forms
from models import db, Alumnos
from flask_migrate import Migrate, migrate 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros_bp)
db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app,db)


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
            apellidos=create_form.aPaterno.data,
            email=create_form.email.data,
            telefono=create_form.email.data
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


@app.route("/modificar", methods=['GET','POST'])
def modificar():
	create_form=forms.UserForm(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alumn=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alumn.nombre
		create_form.apellidos.data=alumn.apellidos
		create_form.email.data=alumn.email
		create_form.telefono.data=alumn.telefono
	if request.method=='POST':
		id=create_form.id.data
		alumn=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alumn.id=id
		alumn.nombre=str.rstrip(create_form.nombre.data)
		alumn.apellidos=create_form.apellidos.data
		alumn.email=create_form.email.data
		alumn.telefono=create_form.telefono.data
		db.session.add(alumn)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("modificar.html",form=create_form)


@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
        
    if request.method == 'POST': 
         id = create_form.id.data
         alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
         db.session.delete(alumn1)
         db.session.commit()
         return redirect(url_for('index'))
         
    return render_template("eliminar.html", form = create_form)


@app.errorhandler(404)
def error(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	csrf.init_app(app)
     
	with app.app_context():
		db.create_all()
	app.run()
