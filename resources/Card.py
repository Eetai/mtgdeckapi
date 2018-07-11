from flask import jsonify, request
from flask_restful import Resource
from Model import db, Deck, DeckSchema, Card, CardSchema, DeckCards, DeckCardsSchema, Event, EventSchema

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
deckscards_schema = DeckCardsSchema(many=True)
decks_schema = DeckSchema(many=True)
events_schema = EventSchema(many=True)


class AllCardsResource(Resource):
    def get(self):
                cards = Card.query.all()
                cards = events_schema.dump(cards).data
                return {"status": "success", "cards": cards}

class CardResource(Resource):
    def get(self, card_id=None):

            card = Card.query.filter(card_id == Card.id)
            card = cards_schema.dump(card).data

            decks_using_card = DeckCards.query.filter(card_id == DeckCards.card_id)
            decks_using_card = deckscards_schema.dump(decks_using_card).data
            deck_ids = [deck['deck_id'] for deck in decks_using_card]

            decknames_using_card = Deck.query.filter(Deck.id.in_(deck_ids))
            decknames_using_card = decks_schema.dump(decknames_using_card).data

            event_list = [deck['event_id'] for deck in decknames_using_card]
            events = Event.query.filter(Event.id.in_(event_list))
            events = events_schema.dump(events).data
            event_name = {event['id']: event for event in events}

            for deck in decknames_using_card:
                event_id = deck['event_id']
                event = event_name[int(event_id)]
                deck['event'] = event
            
            return {"status":"success", "card":card, "decks": decknames_using_card}, 200

# Add main vs sideboard vs both