from pra_site import db

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sonar_org_key = db.Column(db.String, unique=True, nullable=False)
    jenkins_server = db.Column(db.String, unique=True, nullable=False)

    # def __repr__(self):
    #     return f"Project('{self.name}')"
    