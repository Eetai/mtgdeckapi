from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import uuid

ma = Marshmallow()
db = SQLAlchemy()


class Deck(db.Model):
    __tablename__ = 'deck'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    event = db.relationship('Event', backref=db.backref('Decks', lazy='dynamic' ))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, deck, event_id):
        self.deck = deck
        self.event_id = event_id

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=True)
    url = db.Column(db.String(150), unique=False, nullable=True)
    top8url = db.Column(db.String(150), unique=False, nullable=True)
    date = db.Column(db.String(150), unique=False, nullable=True)
    format = db.Column(db.String(150), unique=False, nullable=True)
    season = db.Column(db.String(150), unique=False, nullable=True)
    type = db.Column(db.String(150), unique=False, nullable=True)
    indatabase = db.Column(db.Boolean(), default=False)

    def __init__(self, name):
        self.name = name


class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class DeckCards(db.Model):
    __tablename__ = 'deck_cards'

    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), primary_key=True)
    main_count = db.Column(db.Integer)
    sideboard_count = db.Column(db.Integer)

class DeckCardsSchema(ma.Schema):
    deck_id = fields.Integer()
    card_id = fields.Integer()
    main_count = fields.Integer()
    sideboard_count = fields.Integer()

class CardSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)

class EventSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    date = fields.String(required=True)
    format = fields.String(required=True)
    season = fields.String(required=True)
    url = fields.String(required=True)
    top8url = fields.String(required=True)
    type = fields.String(required=True)
    indatabase = fields.Boolean(required=True)

class DeckSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    event_id = fields.String(default=1, validate=validate.Length(1))
    name = fields.String(required=True, validate=validate.Length(1))