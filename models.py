from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card(db.Model):
    name = db.Column(db.String(80), unique=True)
    card_number = db.Column(db.Integer, unique=True, nullable=False)
    pin = db.Column(db.Integer, unique=True, nullable=False)
    amount = db.Column(db.Integer, unique=True, nullable=False)
    card_id = db.Column(db.String(120), primary_key=True)
    
class Transaction(db.Model):
    transaction_id = db.Column(db.String(120), unique=True, primary_key=True)
    card_id = db.Column(db.String(120), unique=True, nullable=False)
    transaction_type = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, unique=True, nullable=False)
    date_time = db.Column(db.DateTime, nullable=True)


   
