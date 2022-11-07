from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import User

def email_exists(form, field):
    email = User.query.filter_by(user_email = field.data).first()
    if email:
        raise ValidationError("Email ya existe. !!!")

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(4, 16, message="Between 4 to 16 Characters")])
    email = StringField("E-mail", validators=[DataRequired(), Email(), email_exists])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm", message="Contrasena no coinciden")])
    confirm = PasswordField("confirm", validators=[DataRequired()])
    submit = SubmitField("Registrar")

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    stay_loggedin = BooleanField("Remember Me")
    submit = SubmitField("Login")

#Este formulario que acabo de crear debe ser implementada la vista en routes.py
class ScrapyForm(FlaskForm):
    search_article = StringField("Articulo", validators=[DataRequired()])
    submit = SubmitField("Buscar Articulo")
