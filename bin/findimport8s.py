from importdata import get_all_event_data, get_top8_url, add_cards_to_db, unuploaded_events
import psycopg2
import sys
from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from requests.exceptions import RequestException
from getdecklist import get_decklists, turn_deckdict_into_cards
import re

all_event_data = get_all_event_data()
unuploaded_data = unuploaded_events()
con = psycopg2.connect("host='localhost' dbname='mtgapi'") 
con.autocommit = True
cur = con.cursor()

def card_exists_in_jointable(deck_id, card_id): 
    cur.execute("SELECT * FROM deck_cards WHERE deck_id = %s and card_id = %s", (deck_id, card_id))
    return cur.fetchone() is not None


for event in unuploaded_data:
    try:
        # deconstruct tuple
        eventid = event[0]
        url = str(get_top8_url(event[1]))
        indb = event[2]
        # get decks in the deck dicts
        top8dict = get_decklists(url)
        if top8dict:
            # try to add them to the card table
            add_cards_to_db(turn_deckdict_into_cards(top8dict))
            # iterate across deckdict for deck table
            for deck in top8dict:
                cur.execute("INSERT INTO deck (name, event_id) VALUES(%s, %s);", (deck, eventid))
                for mainside in top8dict[deck]:
                    for card in top8dict[deck][mainside]:
                        cur.execute("SELECT id from deck WHERE name like (%s);", (deck,))
                        deckid = cur.fetchone()
                        cur.execute("SELECT id from card WHERE name like (%s);", (card,))
                        cardid = cur.fetchone()
                        count = top8dict[deck][mainside][card]

                        if mainside == 'main':
                            if card_exists_in_jointable(deckid, cardid):
                                cur.execute("UPDATE deck_cards SET main_count = %s where deck_id = %s and card_id = %s ;", (count, deckid, cardid))
                            else: 
                                cur.execute("INSERT INTO deck_cards (deck_id, card_id, main_count) VALUES(%s, %s, %s);", (deckid, cardid, count))

                        if mainside == 'sideboard':
                            if card_exists_in_jointable(deckid, cardid):
                                cur.execute("UPDATE deck_cards SET sideboard_count = %s where deck_id = %s and card_id = %s ;", (count, deckid, cardid))
                            else: 
                                cur.execute("INSERT INTO deck_cards (deck_id, card_id, sideboard_count) VALUES(%s, %s, %s);", (deckid, cardid, count))

            cur.execute("UPDATE events SET indatabase = True WHERE id = %s;", (eventid,))
    except:
        print("Nope")