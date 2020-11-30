from flask import Flask, render_template, flash, url_for, redirect

from forms import InputForm
from models import Project
from pra_site import app

@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = InputForm()
    if form.validate_on_submit():
        flash(f'Your project is registered successfully.', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)

@app.route("/about")
def about():
    return render_template("about.html", title='About')
