from bs4 import BeautifulSoup, SoupStrainer
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import time


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


def get_links():
    url = 'https://magic.wizards.com/en/events/coverage'
    response = simple_get(url)

    soup = BeautifulSoup(response, 'html.parser')
    links = []
 
    for link in soup.findAll('a', attrs={'href': re.compile("")}):
        links.append(link.get('href'))

    events = [event for event in links if "/events/" in event]
    events = [item if 'http' in item else 'https://magic.wizards.com' + item for item in events ]
    with open('events.txt', 'w') as file_handler:
        for item in events:
                file_handler.write("{}\n".format(item))

    return events

def get_top8(event):
    response = simple_get(event)
    soup = BeautifulSoup(response, 'html.parser')
    links = []
 
    for link in soup.findAll('a', attrs={'href': re.compile('')}):
        links.append(link.get('href'))
    top8 = [event for event in links if event.find("top-8-decklists")]
    if len(top8) > 0:
        return top8[0]





