from .db import db

class Balance(db.Document):
    #name = db.ListField(db.StringField(), required=True)
    name = db.StringField(required=True, unique=True)
    balance = db.StringField(required=True, unique=True)
  