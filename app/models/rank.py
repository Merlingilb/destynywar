from app import db

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.String(4096))
    allowed_to_invite = db.Column(db.Boolean, default=False)
    allowed_to_change_ranks = db.Column(db.Boolean, default=False)
    allowed_to_change_name_and_desc = db.Column(db.Boolean, default=False)
    default_rank = db.Column(db.Boolean, default=False)
    alliance_id = db.Column(db.Integer, db.ForeignKey("alliance.id"))

    users = db.relationship("User", backref="alliance_rank", lazy='dynamic', foreign_keys="User.alliance_rank_id")

    def __repr__(self):
        return "<Rank {}>".format(self.name)