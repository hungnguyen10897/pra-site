from flask import Flask, render_template, flash, url_for, redirect, jsonify
from sqlalchemy import func, MetaData, Table, select
import os

from pra_site.forms import InputForm, DownloadForm
from pra_site.models import Source
from pra_site import app, db, engine
from pra_site.utils import format_jenkins_server


@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = InputForm()
    if form.validate_on_submit():
        sonar_org_key = form.sonar_org_key.data
        jenkins_server = format_jenkins_server(form.jenkins_server.data)

        org_sources = Source.query.filter_by(sonar_org_key=sonar_org_key).all()
        server_sources = Source.query.filter_by(jenkins_server=jenkins_server).all()

        if org_sources != [] and server_sources != []:
            orgs_batch_num = org_sources[0].batch_number
            servers_batch_num = server_sources[0].batch_number

            # if same batch won't add
            if orgs_batch_num != servers_batch_num:
                (small, big) = (orgs_batch_num, servers_batch_num) if orgs_batch_num < servers_batch_num else (servers_batch_num, orgs_batch_num)
            
                big_sources = Source.query.filter_by(batch_number = big).all()
                for s in big_sources:
                    s.batch_number = small
                db.session.commit()
            else:
                flash(f'Your link is not registered since the key and server are already in the same batch.', 'success')
        else:
            if org_sources == [] and server_sources == []:
                max_batch = db.session.query(func.max(Source.batch_number)).scalar()
                if max_batch is None:
                    batch_num = 0
                else:
                    batch_num = max_batch + 1
            elif server_sources == []:
                batch_num = org_sources[0].batch_number

            elif org_sources == []:
                batch_num = server_sources[0].batch_number

            source = Source(sonar_org_key=sonar_org_key, jenkins_server=jenkins_server, batch_number = batch_num)
            db.session.add(source)
            db.session.commit()
            flash('Your link is registered successfully.', 'success')

        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

def get_projects(organization):
    connection = engine.connect()
    metadata = MetaData()
    sonar_analyses = Table("sonar_analyses", metadata, autoload=True, autoload_with=engine)

    query = select([sonar_analyses.columns.project.distinct()]).where(sonar_analyses.columns.organization == organization)

    res = connection.execute(query)
    res_set = res.fetchall()

    return list(map(lambda e: e[0], res_set))

@app.route("/download", methods = ["GET", "POST"])
def download():
    form = DownloadForm()
    form.project.choices = get_projects(form.organization.choices[0])
    if form.validate_on_submit():
        organization = form.organization.data
        
    return render_template("download.html", title='Download', form = form)

@app.route("/project/<organization>")
def project(organization):

    projects = get_projects(organization)
    project_array = []
    for name in projects:
        project_obj = {}
        project_obj["name"] = name
        project_array.append(project_obj)
    
    return jsonify({"projects" : project_array})
