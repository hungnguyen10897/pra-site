from pra_site import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    sonarcloud_link = db.Column(db.String, unique=True, nullable=False)
    jenkins_link = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"Project('{self.name}')"
    