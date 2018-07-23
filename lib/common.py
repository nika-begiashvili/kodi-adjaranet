from lib import plugin,utils
import xbmcgui
import xbmcplugin
import xbmc
import re
from BeautifulSoup import BeautifulSoup

urlRegex = re.compile(r"""movieUrlEmpty\s*=\s*[\'\"](.+)[\'\"]""")
langsRegex = re.compile(r"""movieLangs\s*=\s*[\'\"](.+)[\'\"]""")
qualityRegex = re.compile(r"""movieQuals\s*=\s*[\'\"](.+)[\'\"]""")

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
        match = re.search(langsRegex, htmlData)
        langs = match.group(1).split(',')

        if mode == TYPE_MOVIE:
            match  = re.search(qualityRegex, htmlData)
            quality = max( [int(x) for x in match.group(1).split(',')] )
            match = re.search(urlRegex, htmlData)
            url = match.group(1)
            info = utils.getInfo(BeautifulSoup(htmlData))

        for lang in langs:
            url = plugin.buildUrl({'mode': mode, 'id': movieId, 'lang': lang})
            li = utils.listItem(movieId,lang)
            if mode == TYPE_MOVIE:
                url = match.group(1).replace('{lang}', lang).replace('{quality}', str(quality))
                li.setInfo('video', {
                    'title': info['showTitle'],
                    'imdbnumber': info['imdbNumber'],
                })
                li.setProperty('IsPlayable', 'True')
                xbmcplugin.addDirectoryItem(
                    handle=plugin.handle, url=url, listitem=li, isFolder=False)
            else:
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
