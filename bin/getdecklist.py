from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def match_class(target):                                            
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match                                                             

def turn_deckdict_into_cards(deckdict):
    """
    Turns a deckdict object into a list of cards
    """
    cards = []
    for deck in deckdict:
        for mainside in deckdict[deck]:
            for card in deckdict[deck][mainside]:
                    cards.append(card)
    return cards

def get_decklists(event):
    """
    Scrapes a typical wizards MTG decklist page and returns it as a dictionary option
    """
    response = simple_get(event)
    deckdict = {}
    soup = BeautifulSoup(response, 'html.parser')
    decks = soup.findAll("div", attrs={'class':'deck-group'})
    for deck in decks:
        newdeck = {}
        try:
            name = deck.find("h4").text
            main = {}
            main_deck = deck.find("div", attrs={'class':'sorted-by-overview-container'})
            cards = main_deck.find_all('span', {'class' : 'row'})
            for card in cards:
                cardnumber = card.find('span', {'class' : 'card-count'}).text
                cardname = card.find('span', {'class' : 'card-name'}).text
                main[cardname] = cardnumber
            newdeck['main'] = main

            sideboard = {}
            sideboard_deck = deck.find("div", attrs={'class':'sorted-by-sideboard-container'})
            if sideboard_deck:
                sideboard_cards = sideboard_deck.find_all('span', {'class' : 'row'})
                for card in sideboard_cards:
                    cardnumber = card.find('span', {'class' : 'card-count'}).text
                    cardname = card.find('span', {'class' : 'card-name'}).text
                    sideboard[cardname] = cardnumber
            newdeck['sideboard'] = sideboard   
            deckdict[name] = newdeck
        except:
            print("Unable to parse this website")
    return deckdict



