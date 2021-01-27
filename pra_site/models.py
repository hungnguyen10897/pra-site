from pra_site import db
from datetime import datetime

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sonar_org_key = db.Column(db.String, unique=False, nullable=False)
    jenkins_server = db.Column(db.String, unique=False, nullable=False)
    batch_number = db.Column(db.Integer, unique=False, nullable=False, default = 0)
    input_date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.now())
    # to be updated later by data processing pipelines
    # latest_processed_date
     

    def __repr__(self):
        return f"Source('{self.sonar_org_key}' - '{self.jenkins_server}')"
