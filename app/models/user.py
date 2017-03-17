from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.holomail import Holomail


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True)
    password = db.Column(db.String(128))
    chat = db.Column(db.Boolean, default=False)
    planets = db.relationship('Planet', back_populates='owner')

    mail_sent = db.relationship("Holomail", backref="sender", lazy="dynamic", foreign_keys="Holomail.sender_id")
    mail_received = db.relationship("Holomail", backref="receiver", lazy="dynamic", foreign_keys="Holomail.receiver_id")
    mails_sent = db.relationship("Holomailcourse", backref="sender", lazy="dynamic", foreign_keys="Holomailcourse.sender_id")
    mails_received = db.relationship("Holomailcourse", backref="receiver", lazy="dynamic", foreign_keys="Holomailcourse.receiver_id")

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

    def wants_chat(self):
        return self.chat;

    def get_id(self):
        return str(self.id)

    def validate(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def allowed_to_read(self, course):
        if course.sender == self or course.receiver == self:
            return True
        return False

    def has_read_all_mails(self):
        for course in self.mails_received:
            if not course.read_receiver:
                return False
        for course in self.mails_sent:
            if not course.read_sender:
                return False
        return True

    def __repr__(self):
        return "<User {}>".format(self.username)

    def all_mails_read(self):
        for course in self.mails_received:
            if not course.read_receiver:
                return False
        for course in self.mails_sent:
            if not course.read_sender:
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
