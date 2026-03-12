from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Cursos, Maestros, Inscripcion, Alumnos
import forms

cursos_bp = Blueprint('cursos', __name__)

@cursos_bp.route("/indexCursos")
def index():
    cursos_lista = Cursos.query.all()
    print(f"Cursos encontrados: {len(cursos_lista)}") 
    return render_template("indexCursos.html", curso=cursos_lista)

@cursos_bp.route("/nuevoCurso", methods=['GET', 'POST'])
def nuevo_curso():
    create_form = forms.CursoForm(request.form)
   
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") 
                                      for m in Maestros.query.all()]
    
    if request.method == 'POST' and create_form.validate():
        cur = Cursos(
            id=create_form.id.data,
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )
        db.session.add(cur)
        db.session.commit()
        return redirect(url_for('cursos.index'))
        
    return render_template("Cursos.html", form=create_form)

@cursos_bp.route("/modificarCurso", methods=['GET','POST'])
def modificar():
    id = request.args.get('id')
    curso = db.session.query(Cursos).filter(Cursos.id == id).first()
    
    # Usamos request.form para capturar los datos del envío
    create_form = forms.CursoForm(request.form, obj=curso) 
    
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") 
                                      for m in Maestros.query.all()]
    
    if request.method == 'POST':
        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data
        db.session.commit()
        return redirect(url_for('cursos.index'))
    
    # Aquí es donde estaba el error: debe decir "modificarCursos.html"
    return render_template("modificarCursos.html", form=create_form)

@cursos_bp.route("/eliminarCurso", methods=['GET', 'POST'])
def eliminar():
    id = request.args.get('id')
    curso = db.session.query(Cursos).filter(Cursos.id == id).first()
    
    # Creamos el formulario y lo llenamos con los datos del curso para que Jinja lo vea
    create_form = forms.CursoForm(obj=curso) 
    
    if request.method == 'POST': 
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('cursos.index'))
    
    # IMPORTANTE: Pasamos tanto el curso como el form
    return render_template("eliminarCursos.html", curso=curso, form=create_form)

@cursos_bp.route("/detallesCurso")
def detalles():
    id = request.args.get('id')
    curso = db.session.query(Cursos).filter(Cursos.id == id).first()
    if not curso:
        return redirect(url_for('cursos.index'))
    return render_template("detallesCurso.html", curso=curso)

@cursos_bp.route("/inscribir", methods=['GET', 'POST'])
def inscribir():
    form = forms.InscripcionForm(request.form)
    
    # Llenamos los selectores con los datos actuales de la BD
    form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in Alumnos.query.all()]
    form.curso_id.choices = [(c.id, c.nombre) for c in Cursos.query.all()]
    
    if request.method == 'POST' and form.validate():
        nueva_inscripcion = Inscripcion(
            alumno_id=form.alumno_id.data,
            curso_id=form.curso_id.data
        )
        try:
            db.session.add(nueva_inscripcion)
            db.session.commit()
            # Mensaje de éxito (opcional si usas flash)
            return redirect(url_for('cursos.index'))
        except:
            db.session.rollback()
            # Aquí podrías manejar si el alumno ya está inscrito (UniqueConstraint)
            return "Error: El alumno ya está inscrito en este curso."
            
    return render_template("inscribir.html", form=form)

@cursos_bp.route("/verAlumnosCurso/<int:id>")
def ver_alumnos(id):
    # Buscamos el curso para mostrar su nombre en el título
    curso = Cursos.query.get_or_404(id)
    # Accedemos a los alumnos a través de la relación definida en tu modelo
    # (Asumiendo que tienes la relación 'alumnos' configurada en el modelo Cursos)
    alumnos_inscritos = curso.alumnos 
    
    return render_template("verAlumnosCurso.html", curso=curso, alumnos=alumnos_inscritos)