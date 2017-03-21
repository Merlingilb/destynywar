from datetime import datetime
from app import app, db
from flask import render_template, g, abort, flash, redirect, url_for
from app.models.holomail import Holomail
from app.models.holomailcourse import Holomailcourse
from app.models.user import User
from flask_login import login_required
from app.forms.mailform import MailForm
from sqlalchemy import or_, and_


@app.route("/holopost")
@app.route("/holopost/<int:page><string:order><string:direction>")
@login_required
def holopost(page=1,order='time',direction='d'):
    if direction=="d":
        if order=="sender":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).join(User, Holomailcourse.sender).order_by(User.username.desc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).join(User, Holomailcourse.receiver).order_by(User.username.desc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).order_by(Holomailcourse.timestamp.desc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).order_by(Holomailcourse.read_receiver.desc(),Holomailcourse.read_sender.desc()).paginate(page, 10, False)
    elif direction=="a":
        if order=="sender":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).join(User, Holomailcourse.sender).order_by(User.username.asc()).paginate(page, 10, False)
        elif order=="receiver":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).join(User, Holomailcourse.receiver).order_by(User.username.asc()).paginate(page, 10, False)
        elif order=="time":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).order_by(Holomailcourse.timestamp.asc()).paginate(page, 10, False)
        elif order=="read":
            mails = Holomailcourse.query.filter(or_(and_(Holomailcourse.receiver == g.user, Holomailcourse.deleted_receiver == False),and_(Holomailcourse.sender == g.user, Holomailcourse.deleted_sender == False))).order_by(Holomailcourse.read_receiver.asc(),Holomailcourse.read_sender.asc()).paginate(page, 10, False)
    return render_template("holomail.html", title="Holopost", mails=mails)


@app.route("/holopost/view/<int:id>")
@login_required
def holopost_detail(id):
    course = Holomailcourse.query.filter_by(id=id).first()
    if course and g.user.allowed_to_read(course):
        if g.user == course.receiver:
            course.read_receiver = True
            db.session.commit()
        if g.user == course.sender:
            course.read_sender = True
            db.session.commit()
        mails = Holomail.query.filter_by(course_id=course.id).order_by(Holomail.timestamp.desc()).all()
        return render_template("holomail_detail.html", title="Holopost", mails=mails, course=course)
    else:
        return abort(403)

@app.route("/holopost/view/<int:id>/delete")
@login_required
def holopost_delete(id):
    course = Holomailcourse.query.filter_by(id=id).first()
    if course and g.user.allowed_to_read(course):
        course.delete(g.user)
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
                        body="\n"+form.body.data)
        course = Holomailcourse.query.filter_by(sender_id=g.user.id, receiver_id=receiver.id).first()
        if not course:
            course = Holomailcourse.query.filter_by(receiver_id=g.user.id, sender_id=receiver.id).first()
            if not course:
                course = Holomailcourse(receiver=receiver, sender=g.user, timestamp=datetime.now(), read_sender = True, read_receiver = False, deleted_sender = False, deleted_receiver = False)
                course.mails.append(mail)
                db.session.add(course)
            else:
                course.timestamp=datetime.now()
                course.read_sender = False
                course.read_receiver = True
                course.deleted_sender = False
                course.deleted_receiver = False
                course.mails.append(mail)
        else:
            course.timestamp=datetime.now()
            course.read_sender = True
            course.read_receiver = False
            course.deleted_sender = False
            course.deleted_receiver = False
            course.mails.append(mail)
        db.session.add(mail)
        db.session.commit()
        flash("Holopost gesendet!")
        return redirect(url_for("holopost"))
    return render_template("holomail_send.html", title="Holomail Senden", form=form)

