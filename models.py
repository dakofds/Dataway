from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(50), nullable=False)  # <-- Adicionado
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(450))
    author = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(20), nullable=False)

    replies = db.relationship('Reply', backref='item', lazy=True)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)