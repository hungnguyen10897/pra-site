from pra_site import db

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sonar_org_key = db.Column(db.String, unique=False, nullable=False)
    jenkins_server = db.Column(db.String, unique=False, nullable=False)
    # to be updated later by data processing pipelines
    # latest_processed_date
     

    def __repr__(self):
        return f"Source('{self.sonar_org_key}' - '{self.jenkins_server}')"
    