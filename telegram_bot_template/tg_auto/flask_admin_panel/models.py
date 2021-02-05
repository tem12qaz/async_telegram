from .app import db

from sqlalchemy import Enum
import enum

from flask_security import UserMixin, RoleMixin

class Types_of_message(enum.Enum):
    text = 'Text'
    image = 'Image'
    video = 'Video'
    document = 'Document'
    audio = 'Audio'

answer_relation = db.Table('answer_relation',
    db.Column('block_id', db.Integer, db.ForeignKey('block.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
)

message_relation = db.Table('message_relation',
    db.Column('block_id', db.Integer, db.ForeignKey('block.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_answer = db.relationship('Answer', backref='next_message_block')
    messages = db.relationship('Message', secondary=message_relation, backref=db.backref('block', lazy='dynamic'))
    answers = db.relationship('Answer', secondary=answer_relation, backref=db.backref('block', lazy='dynamic'))
    default_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    default = db.relationship('Block', remote_side=[id])
    function_name = db.Column(db.String(255), default=None)

    def __repr__(self):
        return '<Block Message id: {}>'.format(self.id)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    button = db.Column(db.Boolean, default=True)
    next_message_id = db.Column(db.Integer, db.ForeignKey('block.id'))

    def __repr__(self):
        data = (self.text[:30] + '..') if len(self.text) > 32 else self.text
        return '<Answer text: {}>'.format(data)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(Types_of_message))
    content = db.Column(db.Text)

    def __repr__(self):
        data = (self.content[:30] + '..') if len(self.content) > 32 else self.content
        return '<Message content: {}>'.format(data)

class Telegram_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    message_id =  db.Column(db.Integer)

#FLASK-SECURITY
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
