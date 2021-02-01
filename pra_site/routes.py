from flask import Flask, render_template, flash, url_for, redirect, jsonify, send_file, abort
from sqlalchemy import func, MetaData, Table, select
import os, zipfile, glob, subprocess
from pathlib import Path

from pra_site.forms import InputForm, DownloadForm
from pra_site.models import Source
from pra_site import app, db, engine
from pra_site.utils import format_jenkins_server, get_proper_file_name


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
    
    # Getting organizations from Database
    connection = engine.connect()
    metadata = MetaData()
    sonar_analyses = Table("sonar_analyses", metadata, autoload=True, autoload_with=engine)

    query = select([sonar_analyses.columns.organization.distinct()])
    res = connection.execute(query)
    res_set = res.fetchall()

    organizations = list(map(lambda e : e[0], res_set))

    form.organization.choices = list(zip(organizations, organizations))
    form.project.choices = get_projects(form.organization.choices[0][0])

    if form.validate_on_submit():
        return redirect(url_for('download_data', organization = form.organization.data, project_name = form.project.data))

    return render_template("download.html", title='Download', form = form)

@app.route("/download_data/<organization>/<project_name>")
def download_data(organization, project_name):

    project_file_name = get_proper_file_name(project_name)
    
    # Remove old files in /tmp/pra_site/ dir
    for old_file in glob.glob("/tmp/pra_site/*"):
        os.remove(old_file)

    Path('/tmp/pra_site').mkdir(exist_ok=True, parents=True)
    file_path = Path('/tmp/pra_site').joinpath(f"{project_file_name}.zip")
    zip_file = zipfile.ZipFile(file_path,'w', compression = zipfile.ZIP_DEFLATED)

    os.chdir('/tmp/pra_site')

    for type_ in ["analyses", "issues", "measures"]:
        # Download relevant csv files from 130.230.52.209
        subprocess.run([
            "scp", \
            f"130.230.52.209:/mnt/sonar_miner/sonar_data/{type_}/{project_file_name}.csv", \
            f"/tmp/pra_site/{project_file_name}_{type_}.csv" \
        ])
        # /mnt/pra/data/sonarcloud/{organization}           //This should be the right location, temporary solution

        # Only write if there is corresponding type_
        if Path(f"./{project_file_name}_{type_}.csv").exists():
            # Writing to zip file
            zip_file.write(f"{project_file_name}_{type_}.csv")

    zip_file.close()

    return send_file(file_path, mimetype='zip')

@app.route("/project/<organization>")
def project(organization):

    projects = get_projects(organization)
    project_array = []
    for name in projects:
        project_obj = {}
        project_obj["name"] = name
        project_array.append(project_obj)
    
    return jsonify({"projects" : project_array})
