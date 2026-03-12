from flask import Blueprint
from models import db, Maestros
import forms
from flask import Flask, render_template, request, redirect, url_for, flash, g


maestros_bp = Blueprint('maestros', __name__)



@maestros_bp.route("/indexMaestro")
def index():
    create_form = forms.UserForm2(request.form)
    mae = Maestros.query.all() 
    return render_template("indexMaestro.html", form = create_form, mae=mae)


@maestros_bp.route("/maestros", methods=['GET', 'POST'])
def maestros():
    create_form = forms.UserForm2(request.form) 
    
    if request.method == 'POST':
        mae = Maestros(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            especialidad=create_form.especialidad.data 
        )
        db.session.add(mae)
        db.session.commit()     
        return redirect(url_for('maestros.index')) 
    
    return render_template("Maestros.html", form=create_form)

@maestros_bp.route("/detallesMae", methods=['GET', 'POST'])
def detallesMae():
    mat = request.args.get('matricula')
    
    if mat:
        mae1 = db.session.query(Maestros).filter(Maestros.matricula == mat).first()
        
        if mae1:
            return render_template("detallesMae.html", mae=mae1)
    
    return redirect(url_for('maestros.index'))


@maestros_bp.route("/modificarMae", methods=['GET','POST'])
def modificarMae():
    # Buscamos la matrícula en la URL o en el formulario enviado
    matricula = request.args.get('matricula') or request.form.get('matricula')
    mae = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
    
    if not mae:
        return redirect(url_for('maestros.index'))

    # Inicializamos el formulario con los datos recibidos
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'POST' and create_form.validate():
        # Actualizamos directamente la instancia 'mae'
        mae.nombre = create_form.nombre.data
        mae.apellidos = create_form.apellidos.data
        mae.email = create_form.email.data
        mae.especialidad = create_form.especialidad.data
        
        # SQLAlchemy detecta el cambio en el objeto existente y hace un UPDATE
        db.session.commit()
        return redirect(url_for('maestros.index'))
    
    # Si es GET, cargamos los datos actuales en el formulario
    if request.method == 'GET':
        create_form = forms.UserForm2(obj=mae)
            
    return render_template("modificarMae.html", form=create_form)


@maestros_bp.route("/eliminarMae", methods=['GET', 'POST'])
def eliminarMae(): 
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        mae1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if mae1:
            create_form.matricula.data = mae1.matricula
            create_form.nombre.data = mae1.nombre
            create_form.apellidos.data = mae1.apellidos
            create_form.email.data = mae1.email
            create_form.especialidad.data = mae1.especialidad
        else:
            return redirect(url_for('maestros.index'))
            
    if request.method == 'POST': 
         matricula = create_form.matricula.data
         mae1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
         
         if mae1:
             db.session.delete(mae1)
             db.session.commit()
             
         return redirect(url_for('maestros.index'))
         
    return render_template("eliminarMae.html", form = create_form)
