from lib import common,plugin,utils
import xbmcgui
import xbmcplugin

CATEGORY_MAP = {
    'new_release': 'Search/SearchResults?ajax=1&display=15&startYear=1900&endYear=2018&offset=0&orderBy=date&order%5Border%5D=data&order%5Bdata%5D=premiere&order%5Bmeta%5D=desc',
    'top_movies': 'Search/SearchResults?ajax=1&display=15&startYear=1900&endYear=2018&offset=15&orderBy=date&order%5Border%5D=data&order%5Bdata%5D=views&order%5Bmeta%5D=views-week'
}

def get_movie_type(type):
    if type == 1:
        return common.TYPE_MOVIE
    elif type == 3:
        return common.TYPE_SEASONS
    else:
        return common.TYPE_EPISODES

def build_kodi_list_item(movie_type, poster, title):
    li = xbmcgui.ListItem(title, poster)
    if movie_type == common.TYPE_MOVIE:
        playable = 'True'
    else:
        playable = 'False'
    li.setProperty('IsPlayable', playable)
    return li

def loadCategory(category):
    try:
        data = utils.getJsonObject( CATEGORY_MAP[category] )
        for item in data['data']:
            url = plugin.buildUrl({'mode': common.TYPE_MOVIE, 'id': id})
            li = build_kodi_list_item(get_movie_type(
                1), item['poster'], item['title_en'])

            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=False)

    except Exception, e:
        plugin.log('error loading category %s \n %s' %(category, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)