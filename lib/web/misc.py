from bs4 import BeautifulSoup
import requests, time


def get( url, repeat = 6, sleep = 3, soup = False ):

    result = requests.get( url )
    trial = 0
    while not result.ok and trial < repeat:
        result = requests.get( url )
        trial += 1
        time.sleep( sleep )

    if trial == repeat:
        raise RuntimeError( 'Connection failed.' )

    content = result.text
    result.close()

    if soup:
        return BeautifulSoup( content, 'html.parser' )
    else:
        return content
