from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, ValidationError
import jenkins, requests
from sqlalchemy import func, MetaData, Table, select

from pra_site import engine

class InputForm(FlaskForm):
    sonar_org_key = StringField('Sonarcloud Organization Key', validators=[DataRequired()])
    jenkins_server = StringField('Jenkins Server Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')

    def validate_sonar_org_key(self, sonar_org_key):
        r = requests.get(f"https://sonarcloud.io/api/projects/search?organization={sonar_org_key.data}")
        print(r.status_code)
        # organization key exists
        if r.status_code == 404:
            raise ValidationError(f"Organization Key '{sonar_org_key.data}' does not exists.")
            # r = r.json()
            # if 'errors' in r and r['errors'][0]:
            #     error_0 = r['errors'][0]
            #     if 'msg' in error_0 and "No organization for key" in error_0['msg']:
                    # raise ValidationError(f"Organization Key '{sonar_org_key.data}' does not exists.")
        
        # Only adding the Organization key when 403 or 200
        elif r.status_code not in [403, 200]:
            raise ValidationError(f"Something is wrong with Sonarcloud Server or Organiztion Key '{sonar_org_key.data}'")

    def validate_jenkins_server(self, jenkins_server):
        try:
            server = jenkins.Jenkins(jenkins_server.data)
            server.get_version()
        except (KeyError, requests.exceptions.ConnectionError):
            raise ValidationError(f"Jenkins Server '{jenkins_server.data}' does not exist.")

class DownloadForm(FlaskForm):

    organization = SelectField("Sonarqube Organization")
    project = SelectField("Project")
    submit = SubmitField('Download')
    
