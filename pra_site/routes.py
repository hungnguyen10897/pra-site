from flask import Flask, render_template, flash, url_for, redirect

from pra_site.forms import InputForm
from pra_site.models import Source
from pra_site import app, db

@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = InputForm()
    if form.validate_on_submit():
        sonar_org_key = form.sonar_org_key.data
        jenkins_server = form.jenkins_server.data

        sources = Source.query.filter_by(sonar_org_key=sonar_org_key).all()
        # Servers corresponding to thi Sonar Organization
        servers = list(map(lambda s: s.jenkins_server, sources))
        # not yet registered
        if sources == [] or jenkins_server not in servers:
            # Add to DB
            source = Source(sonar_org_key=sonar_org_key, jenkins_server=jenkins_server)
            db.session.add(source)
            db.session.commit()
            flash(f'Your link is registered successfully.', 'success')
        else:
            flash(f"Your combination of Sonarcloud organization key and Jenkins server is already registered.", 'success')

        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template("about.html", title='About')
