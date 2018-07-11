from flask import jsonify, request
from flask_restful import Resource
from Model import db, Deck, DeckSchema

decks_schema = DeckSchema(many=True)
deck_schema = DeckSchema()

class DeckResource(Resource):
    def get(self, deck_id):
            deck = Deck.query.filter(deck_id == Deck.id)
            deck = decks_schema.dump(deck).data
        
            return {"status":"success", "data":deck}, 200