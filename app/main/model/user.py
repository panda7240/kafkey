from .. import db
import json


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    real_name = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    type = db.Column(db.Integer)
    state = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))
    note = db.Column(db.String(1024))

    def to_dictionary(self):
        d = dict()
        d["id"] = self.id
        d["name"] = self.name
        d["password"] = self.password
        d["real_name"] = self.real_name
        d["mail"] = self.mail
        d["phone"] = self.phone
        d["type"] = self.type
        d["state"] = self.state
        d["create_time"] = self.create_time
        d["update_time"] = self.update_time
        d["note"] = self.note
        return d

    def __repr__(self):
        return json.dumps(self.to_dictionary())

db.create_all()