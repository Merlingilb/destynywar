from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_pagedown.fields import PageDownField

class AllianceForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    description = PageDownField("Beschreibung")
    submit = SubmitField("Erstellen")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class AllianceEditForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    description = PageDownField("Beschreibung")
    submit = SubmitField("Ändern")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

