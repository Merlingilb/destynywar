from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.holomail import Holomail
from app.models.alliance import Alliance, alliance_association_table
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True)
    password = db.Column(db.String(128))
    planets = db.relationship('Planet', back_populates='owner')
    alliance_member = db.relationship("Alliance", back_populates="members", lazy='dynamic', secondary=alliance_association_table)

    alliance_owner = db.relationship("Alliance", backref="owner", lazy="dynamic", foreign_keys="Alliance.owner_id")
    mails_sent = db.relationship("Holomail", backref="sender", lazy="dynamic", foreign_keys="Holomail.sender_id")
    mails_received = db.relationship("Holomail", backref="receiver", lazy="dynamic",
                                     foreign_keys="Holomail.receiver_id")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def validate(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def allowed_to_read(self, mail):
        if mail.sender == self or mail.receiver == self:
            return True
        return False

    def __repr__(self):
        return "<User {}>".format(self.username)

    def all_mails_read(self):
        for mail in self.mails_received:
            if not mail.read:
                return False
        return True

    @staticmethod
    def from_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username, email, password):
        try:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return True
        except IntegrityError:
            return False
