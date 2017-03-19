from app import app, db
from flask import render_template, g, abort, flash, redirect, url_for
from app.models.alliance import Alliance
from app.models.user import User
from flask_login import login_required
from app.forms.allianceform import AllianceForm
from app.forms.allianceinviteform import AllianceInviteForm


@app.route("/alliance")
@login_required
def alliance():
    alliances = Alliance.query.filter_by(id=g.user.alliance_id).all()
    if alliances==None:
        alliances=None
    return render_template("alliance.html", title="Alliance", alliances=alliances)

@app.route("/alliance/view/<int:id>")
@login_required
def alliance_detail(id):
    alliance = Alliance.query.filter_by(id=id).first()
    members = User.query.filter_by(alliance_id=alliance.id).all()
    for i in members:
        if i.id==g.user.id and alliance:
            return render_template("alliance_detail.html", title="view alliance", alliance=alliance)
    return abort(403)

@app.route("/alliance/invite/<int:id>", methods=["GET", "POST"])
@login_required
def alliance_invite(id):
    alliance = Alliance.query.filter_by(id=id).first()
    if alliance and alliance.owner_id==g.user.id:
        form=AllianceInviteForm()
        if form.validate_on_submit():
            alliance.members.append(User.query.filter_by(username=form.username.data).first())
            db.session.commit()
            flash("Allianz eingeladen!")
            return redirect(url_for("alliance"))
        return render_template("alliance_invite.html", title="Alliance einladen", alliance=alliance, form=form)
    else:
        return abort(403)

@app.route("/alliance_new", methods=["GET", "POST"])
@login_required
def alliance_new():
    if not Alliance.query.filter_by(id=g.user.alliance_id).first():
        form=AllianceForm()
        if form.validate_on_submit():
            alliance = Alliance(owner_id=g.user.id, name=form.name.data, description=form.description.data)
            alliance.members.append(g.user)
            db.session.add(alliance)
            db.session.commit()
            flash("Allianz erstellt!")
            return redirect(url_for("alliance"))
        return render_template("alliance_new.html", title="Allianz erstellen", form=form)
    else:
        return abort(403)
