from app import db

class Holomailcourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    timestamp = db.Column(db.DateTime)

    read_sender = db.Column(db.Boolean, default=False)
    read_receiver = db.Column(db.Boolean, default=False)

    deleted_sender = db.Column(db.Boolean, default=False)
    deleted_receiver = db.Column(db.Boolean, default=False)

    mails = db.relationship("Holomail", backref="course", lazy="dynamic", foreign_keys="Holomail.course_id")

    def delete(self, user):
        if user == self.sender:
            self.deleted_sender = True
        if user == self.receiver:
            self.deleted_receiver = True

    def __repr__(self):
        return "<Holomailverlauf {}>".format(self.id)