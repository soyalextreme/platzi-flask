from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length



class LoginForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired("Ingresa un username")])
    password = PasswordField("Password", validators=[DataRequired("Necesitas una contrasena"), Length(5, 15, "Contrasena Invalida")])
    c_password = PasswordField("Confirm Password", validators=[DataRequired("Necesitas confirmar la contrasena"), ])
    submit = SubmitField("Enviar")
    
    def validate_passwords(form, field, password):
        if field.data != password:
            raise ValidationError("Contrasenas no coinciden")

class TodoForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Crear")

class DeleteTodoForm(FlaskForm):
    submit = SubmitField("Borrar")


class UpdateTodoForm(FlaskForm):
    submit = SubmitField("Actualizar")