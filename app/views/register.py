from flask import render_template, flash, redirect

from app import app
from app.forms.registerform import RegisterForm
from app.models.user import User


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.create_user(form.username.data, form.email.data, form.password.data):
            flash("Account wurde erstellt. Bitte einloggen.")
            return redirect("login")
        else:
            flash("Fehler beim erstellen des Accounts. Möglicherweise war der Accountname schon vergeben.")
    return render_template("register.html", form=form, title="Registrierung")