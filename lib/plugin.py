import urlparse
import urllib
import sys
import xbmcplugin
import xbmc

baseUrl = sys.argv[0]
handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def setContent(content):
    global handle
    xbmcplugin.setContent(handle, content)

def buildUrl(query):
    global baseUrl
    return baseUrl + '?' + urllib.urlencode(query)

def log(arg):
    xbmc.log(arg, xbmc.LOGWARNING)


"""
class Router():

    def  __init__(self,args):
        self.base_url = args[0]
        self.addon_handle = int(args[1])
        self.args = urlparse.parse_qs(args[2][1:])

    def buildUrl(self,query):
        return self.base_url + '?' + urllib.urlencode(query)

    def setContent(self,content):
        xbmcplugin.setContent(self.addon_handle, content)

    def run():
        mode = self.args.get('mode', None)
        if mode is None:
            main_screen()
        elif mode[0] == 'category':
            category = args.get('category', 'new_release')
            load_category(category[0])
        elif mode[0] == 'search':
            search()
        elif mode[0] == TYPE_MOVIE:
            movie_id = args.get('id', None)
            load_movie(movie_id[0])
        elif mode[0] == TYPE_SEASONS:
            xbmc.log('seasons', xbmc.LOGWARNING)
            movie_id = args.get('id', None)
            load_seasons(movie_id[0])
        elif mode[0] == TYPE_EPISODES:
            movie_id = args.get('id', None)
            load_seasons(movie_id[0])"""