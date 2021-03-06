import simplejson as json
from httplib2 import Http
from BeautifulSoup import BeautifulSoup
from lib import plugin
from HTMLParser import HTMLParser
import xbmcgui

API_BASE = 'https://api.adjaranet.com/api/v1/'
STATIC_FILES = 'http://staticnet.adjara.com/'

def getIcon(movieId):
    movieId = str(movieId)
    return STATIC_FILES + 'moviecontent/%s/covers/157x236-%s.jpg' % (movieId, movieId)

def getCover(movieId):
    movieId = str(movieId)
    return STATIC_FILES + 'moviecontent/%s/covers/1920x1080-%s.jpg' % (movieId, movieId)

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

def listItem(movieId,title,isPlayable = False):
    li = xbmcgui.ListItem(title, getIcon(movieId))
    li.setProperty('IsPlayable', str(isPlayable))
    li.setArt({
        'icon': getIcon(movieId),
        'landscape': getCover(movieId)
    })
    return li

def getInfo(htmlObject):
    out = dict()
    showInfo = htmlObject.find('div', {'id': 'movie-info'})
    out['showTitle'] = showInfo.find('h2', {'class': 'originalTitle'}).contents[0]
    out['showTitle'] = HTMLParser().unescape(out['showTitle'])
    imdb = showInfo.find('a', {'class': 'imdb'})
    out['imdbNumber'] = imdb.get('href').split('/')[-1]
    return out
