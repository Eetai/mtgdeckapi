import psycopg2
import sys
from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from requests.exceptions import RequestException
from getdecklist import get_decklists
from scrape import simple_get
import re

def turn_decklist_to_cards(link):
    cards = set()
    top8decks = get_decklists(link)
    for name in top8decks:
        for mainside in top8decks[name]:
            for card in top8decks[name][mainside]:
                cards.add(card)
    return cards

def add_cards_to_db(cards):
    # takes cards as a list
    con = None

    try:
        def exists(name):
            cur.execute("SELECT name FROM card WHERE name = %s", (name,))
            return cur.fetchone() is not None

        con = psycopg2.connect("host='localhost' dbname='mtgapi'")   
        cur = con.cursor()  
        for card in cards:
            if not exists(card):
                cur.execute("INSERT INTO card (name) VALUES(%s);", (card,))
        con.commit()
    finally:
        if con:
            con.close()

def get_all_event_data():
    # returns tuple: (eventid, url, indatabase boolean)
        con = None
        con = psycopg2.connect("host='localhost' dbname='mtgapi'")   
        cur = con.cursor()
        cur.execute("SELECT id, url, indatabase FROM EVENTS")
        data = cur.fetchall()
        return data

def unuploaded_events():
    # returns tuple: (eventid, url, indatabase boolean)
        con = None
        con = psycopg2.connect("host='localhost' dbname='mtgapi'")   
        cur = con.cursor()
        cur.execute("SELECT id, url, indatabase FROM EVENTS where indatabase = False")
        data = cur.fetchall()
        return data

def get_top8_url(event):
    # searches for link to top8 decklist page
    response = simple_get(event)
    soup = BeautifulSoup(response, 'html.parser')
    links = []
 
    for link in soup.findAll('a', attrs={'href': re.compile('')}):
        links.append(link.get('href'))
    top8 = [event for event in links if "top-8-decks" in event]
    if len(top8) > 0:
        print('https://magic.wizards.com' + top8[0])
        return 'https://magic.wizards.com' + top8[0]
    else:
        return None