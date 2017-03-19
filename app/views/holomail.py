from datetime import datetime
from app import app, db
from flask import render_template, g, abort, flash, redirect, url_for
from app.models.holomail import Holomail
from app.models.user import User
from flask_login import login_required
from app.forms.mailform import MailForm


@app.route("/holopost")
@app.route("/holopost/<int:page><string:order><string:direction>")
@login_required
def holopost(page=1,order='time',direction='d'):
    if direction=="d":
        if order=="sender":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.sender.username.desc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.receiver.username.desc()).paginate(page, 10, False)
        elif order=="subject":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.subject.desc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.timestamp.desc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.read.desc()).paginate(page, 10, False)
    elif direction=="a":
        if order=="sender":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.sender.username.asc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.receiver.username.asc()).paginate(page, 10, False)
        elif order=="subject":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.subject.asc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.timestamp.asc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomail.query.filter(Holomail.receiver == g.user, Holomail.deleted_receiver == False).order_by(Holomail.read.asc()).paginate(page, 10, False)
    return render_template("holomail.html", title="Holopost", mails=mails)

@app.route("/holopost/out")
@app.route("/holopost/out/<int:page><string:order><string:direction>")
@login_required
def holopost_sent(page=1,order='time',direction='d'):
    if direction=="d":
        if order=="sender":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.sender.username.desc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.receiver.username.desc()).paginate(page, 10, False)
        elif order=="subject":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.subject.desc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.timestamp.desc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.read.desc()).paginate(page, 10, False)
    elif direction=="a":
        if order=="sender":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.sender.username.asc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.receiver.username.asc()).paginate(page, 10, False)
        elif order=="subject":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.subject.asc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.timestamp.asc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomail.query.filter(Holomail.sender == g.user, Holomail.deleted_sender == False).order_by(Holomail.read.asc()).paginate(page, 10, False)
    return render_template("holomail_sent.html", title="Holopost sent", mails=mails)


@app.route("/holopost/view/<int:id>")
@login_required
def holopost_detail(id):
    mail = Holomail.query.filter_by(id=id).first()
    if mail and g.user.allowed_to_read(mail):
        if g.user == mail.receiver:
            mail.read = True
            db.session.commit()
        return render_template("holomail_detail.html", title="Holopost", mail=mail)
    else:
        return abort(403)

@app.route("/holopost/view/<int:id>/delete")
@login_required
def holopost_delete(id):
    mail = Holomail.query.filter_by(id=id).first()
    if mail and g.user.allowed_to_read(mail):
        mail.delete(g.user)
        db.session.commit()
        return redirect(url_for("holopost"))
    else:
        return abort(403)

@app.route("/holopost/write", methods=["GET", "POST"])
@app.route("/holopost/write/<string:receiver>", methods=["GET", "POST"])
@login_required
def holopost_write(receiver=None):
    user = User.query.filter_by(username=receiver).first()
    if user:
        form = MailForm(receiver=user.username)
    else:
        form = MailForm()

    if form.validate_on_submit():
        receiver = User.query.filter_by(username=form.receiver.data).first()
        mail = Holomail(receiver=receiver, sender=g.user, timestamp=datetime.now(), subject=form.subject.data,
                        body="\n"+form.body.data, read=False, deleted_sender=False, deleted_receiver=False)
        db.session.add(mail)
        db.session.commit()
        flash("Holopost gesendet!")
        return redirect(url_for("holopost"))
    return render_template("holomail_send.html", title="Holomail Senden", form=form)

