#Kopimi -- No license.

from google.appengine.api.memcache import get
from google.appengine.api.memcache import set
from os import environ
from re import compile
from re import match
from urllib import unquote

## LOCAL CACHING

trackers_list = get('trackers_list')
if trackers_list is None:
    trackers_list = ['http://bittrk.appspot.com/announce',
                     'http://nemesis.1337x.org/announce',
                     'http://torrent.ipnm.ru/announce',
                     'http://tracker.bittorrent.am/announce',
                     'http://tracker.openbittorrent.com/announce',
                     'http://tracker.publicbt.com/announce',
                     'https://bittrk.appspot.com/announce',
                     'https://memtracker.appspot.com/announce'].sort()

info_hash_pattern=compile(r".*info_hash=([^?]+).*")

request_counter=0

def main():
    global trackers_list
    global request_counter
    request_counter+=1
    if request_counter > 10000:
        trackers_list = get('trackers_list')
    # GET THE INT VALUE OF THE FIRST BYTE FROM THE HASH INFO
    try:
        urlencoded_info_hash=info_hash_pattern.match(environ['QUERY_STRING']).group(1)
    except:
        urlencoded_info_hash=' '
    first_char = ord(unquote(urlencoded_info_hash)[:1])
    
    tracker = trackers_list[first_char%len(trackers_list)]

    if environ['PATH_INFO'][1:2] == 'a': # FOR ANNOUNCES
        print 'Status: 301 Moved Permanently\nLocation: '+tracker+'?'+environ['QUERY_STRING']+'\n'
    
    elif environ['PATH_INFO'][1:2] == 's': # FOR SCRAPES
        print 'Status: 301 Moved Permanently\nLocation: '+tracker[:-8]+'scrape?'+environ['QUERY_STRING']+'\n'


if __name__ == '__main__':
  main()