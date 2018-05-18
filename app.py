from flask import Flask, render_template, url_for, redirect, flash, request, g

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import *

import datetime
import models
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsflkjadf123'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """loads user"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """opens database for request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """closes database after request"""
    g.db.close()
    return response


@app.route('/register', methods=["GET", "POST"])
def register():
    """registers user allowing user to login"""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('list'))
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """allows user to login"""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password is not correct", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged in!", "success")
                return redirect(url_for("list"))
            else:
                flash("Your email or password is not correct", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """logs user out"""
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for('list'))


@app.route('/')
def index():
    """homepage"""
    return render_template('index.html')


@app.route('/')
@app.route('/entries')
def list():
    """list journal entry post on homepage"""
    try:
        posts = models.Post.select().order_by(-models.Post.date)
    except AttributeError:
        return render_template('index.html')
    return render_template('index.html', posts=posts)


@app.route('/entry', methods=("GET", "POST"))
@login_required
def add_entry():
    """Allows user to add post"""
    form = forms.NewEntry()
    if form.validate_on_submit():
        entry = models.Post.create(
                user_id=g.user.id,
                title=form.title.data,
                date=form.date.data,
                time=form.time.data,
                learned=form.learned.data,
                resources=form.resources.data
                )
        return redirect(url_for('list'))
    return render_template('new.html', form=form)


@app.route('/details/<post>')
def details(post):
    """Shows details of specific post"""
    entry = models.Post.select().where(models.Post.title == post)
    return render_template('detail.html', entry=entry)


@app.route('/edit/<post>', methods=("GET", "POST"))
def edit(post):
    """allows user to change original post as long as
       they are the user that created the original posts
       """
    form = forms.NewEntry()
    entry = models.Post.get(models.Post.title == post)
    entry.delete_instance()
    if form.validate_on_submit():
        update_entry = models.Post.create(
                user_id=g.user.id,
                title=form.title.data,
                date=form.date.data,
                time=form.time.data,
                learned=form.learned.data,
                resources=form.resources.data
        )
        return redirect(url_for('list'))
    return render_template('edit.html', form=form)


@app.route('/delete/<post>')
def delete(post):
    """Allows user to delete a post as long as they are
       the user that initially created the post
    """
    entry = models.Post.get(models.Post.title == post)
    entry.delete_instance()
    return redirect(url_for('list'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True, host='0.0.0.0', port=8000)
