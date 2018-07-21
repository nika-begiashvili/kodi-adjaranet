import simplejson as json
from httplib2 import Http
from BeautifulSoup import BeautifulSoup
from lib import plugin

API_BASE = 'http://net.adjara.com/'
STATIC_FILES = 'http://staticnet.adjara.com/'

def getIcon(movie_id):
    movie_id = str(movie_id)
    return STATIC_FILES + 'moviecontent/%s/covers/157x236-%s.jpg' % (movie_id, movie_id)

def getCover(movie_id):
    movie_id = str(movie_id)
    return STATIC_FILES + 'moviecontent/%s/covers/1920x1080-%s.jpg' % (movie_id, movie_id)

def getResponse(endpoint):
    try:
        (_, rsp) = Http().request(API_BASE + endpoint)
        return rsp
    except Exception, e:
        plugin.log('Error fetching %s \n %s' % (endpoint,str(e)))
        return None

def getJsonObject(endpoint):
    try:
        rsp = getResponse(endpoint)
        return json.loads(rsp)
    except Exception, e:
        plugin.log('Error parsing json %s\n%s\n' % (rsp,str(e)))
        return None

def getHtml(endpoint):
    try:
        rsp = getResponse(endpoint)
        return BeautifulSoup(rsp)
    except Exception, e:
        plugin.log('Error parsing html %s \n %s' % (rsp,str(e)))
        return None