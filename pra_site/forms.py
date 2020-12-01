from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class InputForm(FlaskForm):
    sonar_org_key = StringField('Sonarcloud Organization Key', validators=[DataRequired()])
    jenkins_server = StringField('Jenkins Server Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
