from flask import current_app, jsonify, request, Blueprint
from flask_restful import Resource
from Model import db, Event, EventSchema, Deck, DeckCards, Card, DeckSchema, DeckCardsSchema, CardSchema

events_schema = EventSchema(many=True)
event_schema = EventSchema()
deck_schema = DeckSchema(many=True)
deckcards_schema = DeckCardsSchema(many=True)
card_schema = CardSchema(many=True)


class AllEventsResource(Resource):
    def get(self):
                events = Event.query.all()
                events = events_schema.dump(events).data
                return {"status": "success", "events": events}

class EventResource(Resource):
    def get(self, event_id):
            if event_id == None:
                events = Event.query.all()
                events = events_schema.dump(events).data
                return {"status": "success", "events": events}

            events = Event.query.filter(event_id == Event.id)
            events = events_schema.dump(events).data

            decks = Deck.query.filter(event_id == Deck.event_id)
            decks = deck_schema.dump(decks).data
            deckids = [deck['id'] for deck in decks]
            id_to_name = {deck['id']: deck['name'] for deck in decks}

            deckcards = DeckCards.query.filter(DeckCards.deck_id.in_(deckids))
            decklists = deckcards_schema.dump(deckcards).data

            cardids = [card['card_id'] for card in decklists]
            cards = Card.query.filter(Card.id.in_(cardids))
            cards = card_schema.dump(cards).data

            cards_dict = {card['id'] : card['name'] for card in cards}

            for deck in decklists:
                deck['card_name'] = cards_dict[deck['card_id']]
            decklist_json = {}
            for deck_id in deckids:
                decklist_json[id_to_name[deck_id]] = [card for card in decklists if card['deck_id'] == deck_id]

            return {"status":"success", "event":events, "decks":decklist_json }, 200