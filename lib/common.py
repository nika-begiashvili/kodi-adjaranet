from lib import plugin,utils
import xbmcgui
import xbmcplugin
import xbmc

def addCategory(label, category, iconImage='DefaultFolder.png', url=None):
    if url is None:
        url = plugin.buildUrl({'mode': 'category', 'category': category})
    li = xbmcgui.ListItem(label, iconImage=iconImage)
    xbmcplugin.addDirectoryItem(handle=plugin.handle, url=url,
                                listitem=li, isFolder=True)


def mainScreen():
    addCategory('Search', None, 'DefaultAddonsSearch.png',
                 plugin.buildUrl({'mode': 'search'}))
    addCategory('New Releases', 'new_release')
    addCategory('Top Movies', 'top_movies')
    xbmcplugin.endOfDirectory(plugin.handle)


TYPE_MOVIE = 'movie'
TYPE_SEASONS = 'seasons'
TYPE_EPISODE = 'episode'
TYPE_EPISODES = 'episodes'
TYPE_LANGUAGES = 'langs'

def build_kodi_list_item(movie_type, poster, title):
    li = xbmcgui.ListItem(title, poster)
    if movie_type == TYPE_MOVIE:
        playable = 'True'
    else:
        playable = 'False'
    li.setProperty('IsPlayable', playable)
    return li


def get_movie_type(type):
    if type == 1:
        return TYPE_MOVIE
    elif type == 3:
        return TYPE_SEASONS
    else:
        return TYPE_EPISODES

def search():
    kb = xbmc.Keyboard('', 'Search for movie')
    kb.doModal()
    if (kb.isConfirmed()):
        searchTerm = kb.getText()
    else:
        return

    searchUrl = 'Home/quick_search?ajax=1&search=' + searchTerm
    try:
        data = utils.getJsonObject(searchUrl)
        for item in data['movies']['data']:
            movie_type = get_movie_type(item['type'])
            id = item['id']
            url = plugin.buildUrl({'mode': TYPE_LANGUAGES, 'id': id,
                             'tv_show': movie_type != TYPE_MOVIE})
            li = build_kodi_list_item(
                movie_type, utils.getCover(id), item['title_en'])
            li.setArt({
                'icon': utils.getIcon(id),
                'landscape': utils.getCover(id)
            })
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)
    except Exception, e:
        plugin.log('error searching for %s \n %s' % (searchTerm, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)
