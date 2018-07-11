from flask import Blueprint
from flask_restful import Api
from resources.Deck import DeckResource
from resources.Event import EventResource
from resources.Event import AllEventsResource
from resources.Card import CardResource
from resources.Card import AllCardsResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes

api.add_resource(DeckResource, '/Deck/<string:deck_id>/')
api.add_resource(AllEventsResource, '/Event/')
api.add_resource(EventResource, '/Event/<string:event_id>/')
api.add_resource(AllCardsResource, '/Card/')
api.add_resource(CardResource, '/Card/<string:card_id>/')