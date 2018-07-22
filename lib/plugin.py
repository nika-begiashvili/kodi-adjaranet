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

def getArg(arg, default = None):
    global args
    res = args.get(arg, None)
    if res is None:
        return default
    else:
        return res[0]