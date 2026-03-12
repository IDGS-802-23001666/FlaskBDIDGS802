from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Alumnos
import forms

alumnos_bp = Blueprint('alumnos', __name__)

@alumnos_bp.route("/indexAlumnos")
def index():
    create_form = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)

@alumnos_bp.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alumn = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data, # Usando el nombre de campo de tu forms.py
            email=create_form.email.data,
            telefono=create_form.telefono.data
        )
        db.session.add(alumn)
        db.session.commit()
        return redirect(url_for('alumnos.index'))
    return render_template("Alumnos.html", form=create_form)

@alumnos_bp.route("/detalles", methods=['GET', 'POST'])
def detalles():
    alumn1 = None
    id = request.args.get('id')
    if id:
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    if not alumn1:
        return redirect(url_for('alumnos.index'))
    return render_template("detalles.html", alumn=alumn1)

@alumnos_bp.route("/modificar", methods=['GET','POST'])
def modificar():
    # Buscamos el ID en la URL (GET) o en los datos del formulario (POST)
    id = request.args.get('id') or request.form.get('id')
    alumn = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    
    if not alumn:
        # Si no hay ID o no existe el alumno, regresamos al index
        return redirect(url_for('alumnos.index'))

    # Vinculamos el formulario con los datos que vienen del request
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        # IMPORTANTE: Modificamos la instancia que ya existe
        alumn.nombre = create_form.nombre.data
        alumn.apellidos = create_form.apellidos.data
        alumn.email = create_form.email.data
        alumn.telefono = create_form.telefono.data
        
        # Guardamos los cambios
        db.session.commit()
        return redirect(url_for('alumnos.index'))
    
    # Si es GET, precargamos el formulario con los datos actuales del alumno
    if request.method == 'GET':
        create_form = forms.UserForm(obj=alumn)

    return render_template("modificar.html", form=create_form)

@alumnos_bp.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alumn1:
            create_form.id.data = id
            create_form.nombre.data = alumn1.nombre
            create_form.apellidos.data = alumn1.apellidos
            create_form.telefono.data = alumn1.telefono
            create_form.email.data = alumn1.email
    if request.method == 'POST': 
         id = create_form.id.data
         alumn1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
         db.session.delete(alumn1)
         db.session.commit()
         return redirect(url_for('alumnos.index'))
    return render_template("eliminar.html", form=create_form)