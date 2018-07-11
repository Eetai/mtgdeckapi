from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import pprint
import psycopg2
import sys
from getdecklist import get_decklists

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


def get_events(link):
    response = simple_get(link)
    soup = BeautifulSoup(response, 'html.parser')
    seasons = soup.findAll("div", attrs={'class':'bean_block'})
    count = []
    con = psycopg2.connect("host='localhost' dbname='mtgapi'")   
    cur = con.cursor()  
    for season in seasons:
        season_text = season.find("h2").text
        lines = str(season).split('<br/>')
        for line in lines:
            if len(line.split('</a>')) > 1 and len(line.split('<br/')) > 0:
                data = line.split('</a>')[-1].split('<br/>')[0]
                if data:
                    data = data.split('</p>\n</div>\n</div>')[0]
                    soup = BeautifulSoup(line, 'html.parser')
                    event = soup.find('a', attrs={'href': re.compile('')})
                    if data: 
                        dates = data[data.find("(")+1:data.find(")")]
                        event_type = data.split(") – ")
                        if len(event_type) > 1:
                            event_type = event_type[1]
                        else:
                            event_type = None
                    name = event.text
                    url = event.get('href')
                    if not event_type:
                        event_type = None
                    if not dates:
                        dates = None
                    if not name:
                        name = None
                    if not url: 
                        url = None
                    
                    thefullpackage = (season_text, event_type, dates, name, url)
                    print(thefullpackage)
                    cur.execute("""INSERT INTO events(season, type, date, name, url) VALUES (%s, %s, %s, %s, %s);""", thefullpackage)
                    con.commit()
