from app import db

alliance_association_table = db.Table('alliance_association', db.Model.metadata,
                                     db.Column('alliance_id', db.Integer, db.ForeignKey('alliance.id')),
                                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                                     )

class Alliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.String(4096))

    members = db.relationship("User", backref="alliance", lazy='dynamic', foreign_keys="User.alliance_id")

    def __repr__(self):
        return "<Alliance {}>".format(self.name)
    
