from lib import common,plugin,utils
import xbmcgui
import xbmcplugin

CATEGORY_MAP = {
    'new_release': 'Search/SearchResults?ajax=1&display=15&startYear=1900&endYear=2018&offset=0&orderBy=date&order%5Border%5D=data&order%5Bdata%5D=premiere&order%5Bmeta%5D=desc',
    'top_movies': 'Search/SearchResults?ajax=1&display=15&startYear=1900&endYear=2018&offset=15&orderBy=date&order%5Border%5D=data&order%5Bdata%5D=views&order%5Bmeta%5D=views-week'
}

def loadCategory(category):
    try:
        data = utils.getJsonObject( CATEGORY_MAP[category] )
        for item in data['data']:
            url = plugin.buildUrl({'mode': common.TYPE_LANGUAGES, 'id': item['id']})
            li = utils.listItem(item['id'],item['title_en'])
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)

    except Exception, e:
        plugin.log('error loading category %s \n %s' %(category, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)