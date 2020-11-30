from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length

class InputForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(min=5)])
    sonarcloud_link = StringField('Sonarcloud Link', validators=[DataRequired(), URL()])
    jenkins_link = StringField('Sonarcloud Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
