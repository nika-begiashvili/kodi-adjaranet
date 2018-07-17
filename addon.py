import simplejson as json
from httplib2 import Http
import re
import urllib2
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
find_var_regex = re.compile(r"""movieUrlEmpty\s*=\s*[\'\"](.+)[\'\"]""")

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:

    url = build_url({'mode': 'category', 'category': 'Search'})
    li = xbmcgui.ListItem('Premier', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'category', 'category': 'Premier'})
    li = xbmcgui.ListItem('Premier', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'category':

    cat_url = 'http://net.adjara.com/Search/SearchResults?ajax=1&display=15&startYear=1900&endYear=2018&offset=0&isnew=0&needtags=0&orderBy=date&order%5Border%5D=data&order%5Bdata%5D=premiere&order%5Bmeta%5D=desc'
    json_data = None

    try:
        (rsp_headers, json_data) = Http().request(cat_url)
        data  = json.loads(json_data)
        for item in data['data']:
            url = build_url({'mode': 'movie', 'id': item['id']})
            li = xbmcgui.ListItem(item['title_en'], iconImage=item['poster'])
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    except urllib2.URLError, e:
        xbmcplugin.endOfDirectory(addon_handle)
        xbmc.log('adjaranet: got http error %d fetching %s' % (e.code, api_url), xbmc.LOGWARNING)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'movie':

    movie_id = args.get('id', None)
    script_url = 'http://net.adjara.com/Movie/main?id='+ movie_id[0] +'&js=1'

    try:
        (rsp_headers, html_data) = Http().request(script_url)
        match = re.search(find_var_regex,html_data)
        if not match:
            xbmc.log('can not find url at %s' % (script_url), xbmc.LOGWARNING)
            raise Exception('url not found')
        
        url = match.group(1).replace('{lang}','English').replace('{quality}','1500')
        xbmc.log(url, xbmc.LOGWARNING)
        
        play_item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

    except urllib2.URLError, e:
        xbmc.log('adjaranet: got http error %d fetching %s' % (e.code, api_url), xbmc.LOGWARNING)
