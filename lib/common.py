from lib import plugin,utils
import xbmcgui
import xbmcplugin
import xbmc
import re

langs_regex = re.compile(r"""movieLangs\s*=\s*[\'\"](.+)[\'\"]""")

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

def loadLanguages(movieId, tvShow):
    try:
        scriptUrl ='Movie/main?id=' + movieId + '&js=1'

        if tvShow == 'True':
            scriptUrl = scriptUrl + '&serie=1'
            mode = TYPE_SEASONS
        else:
            mode = TYPE_MOVIE

        htmlData = utils.getResponse(scriptUrl)
        match = re.search(langs_regex, htmlData)
        langs = match.group(1).split(',')

        for lang in langs:
            url = plugin.buildUrl({'mode': mode, 'id': movieId, 'lang': lang})
            li = utils.listItem(movieId,lang)
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=(mode == TYPE_SEASONS))

    except Exception, e:
        plugin.log('error loading languages %s' % (str(e),) )
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)

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
            id = item['id']
            url = plugin.buildUrl({'mode': TYPE_LANGUAGES, 'id': id,
                             'tv_show': item['type'] != 1})
            li = utils.listItem(id,item['title_en'])
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)
    except Exception, e:
        plugin.log('error searching for %s \n %s' % (searchTerm, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)
