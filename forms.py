from wtforms import Form, StringField, IntegerField, EmailField, validators

class UserForm(Form):
    # 'id' en el modelo es 'matricula' en tu lógica visual
    id = IntegerField('Matricula', [
        validators.DataRequired(message="El campo es requerido"),
        # Ajusté el rango para que sea más flexible como una ID de BD
        validators.NumberRange(min=1, max=999999, message="Ingrese una matrícula válida"),
    ])
    
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres")
    ])
    
    aPaterno = StringField("Apellido Paterno", [
        validators.DataRequired(message="El campo es requerido"),
    ])
    
    email = EmailField("Correo", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Ingrese un correo válido"),
    ])