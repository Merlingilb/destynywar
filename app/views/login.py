from app import app, lm
from flask import render_template, flash, url_for, redirect, g
from app.forms.loginform import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.from_username(str(form.username.data))
        if user and user.validate(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return form.redirect("index")
        else:
            flash("Password incorrect.")
    return render_template("login.html", form=form, title="Login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))