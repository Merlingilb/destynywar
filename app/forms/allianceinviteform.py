from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models.user import User
from app.models.alliance import Alliance

def validate_user(form, field):
    user = User.query.filter_by(username=field.data).first()
    if not user:
        raise ValidationError("User does not exist")
    if Alliance.query.filter_by(id=user.alliance_id).first():
        raise ValidationError("User is already in an Alliance")

class AllianceInviteForm(FlaskForm):

    username = StringField("Benutzername", validators=[DataRequired(), validate_user])
    submit = SubmitField("Einladen")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

