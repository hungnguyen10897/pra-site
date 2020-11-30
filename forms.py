from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class InputForm(FlaskForm):
    sonarcloud_link = StringField('Sonarcloud Link', validators=[DataRequired(), URL()])
    jenkins_link = StringField('Sonarcloud Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
