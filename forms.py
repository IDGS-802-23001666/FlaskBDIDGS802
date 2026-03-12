from wtforms import Form, StringField, IntegerField, EmailField, SelectField, TextAreaField, validators
from wtforms import Form, SelectField, validators

class UserForm(Form):
    id = IntegerField('Matricula', [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=999999, message="Ingrese una matrícula válida"),
    ])
    
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres")
    ])
    
    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido"),
    ])
    
    email = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un correo válido"),
    ])

    # Corregido: StringField en lugar de EmailField
    telefono = StringField("Teléfono", [
        validators.DataRequired(message="El campo es requerido"),
    ])

class UserForm2(Form):
    matricula = IntegerField('Matricula', [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=1, max=999999, message="Ingrese una matrícula válida"),
    ])
    
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres")
    ])
    
    apellidos = StringField("Apellidos", [
        validators.DataRequired(message="El campo es requerido"),
    ])
    
    email = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un correo válido"),
    ])

    # Corregido: StringField para especialidad
    especialidad = StringField("Especialidad", [
        validators.DataRequired(message="El campo es requerido"),
    ])

class CursoForm(Form):
    id = IntegerField('ID Curso', [
        validators.DataRequired(message="El campo es requerido"),
    ])
    
    nombre = StringField("Nombre del Curso", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=150, message="El nombre debe tener entre 3 y 150 caracteres") 
    ])
    
    # Usamos TextAreaField para descripciones largas
    descripcion = TextAreaField("Descripción", [
        validators.DataRequired(message="El campo es requerido"),
    ])

    # SelectField para elegir al maestro por su matrícula
    maestro_id = SelectField('Maestro Asignado', coerce=int, validators=[
        validators.DataRequired(message="Debe asignar un maestro")
    ])

class InscripcionForm(Form):
    # SelectFields para vincular registros existentes
    alumno_id = SelectField('Alumno', coerce=int, validators=[
        validators.DataRequired(message="Seleccione un alumno")
    ])
    
    curso_id = SelectField('Curso', coerce=int, validators=[
        validators.DataRequired(message="Seleccione un curso")
    ])

