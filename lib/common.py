from lib import plugin, utils
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
    # addCategory('New Releases', 'new_release')
    # addCategory('Top Movies', 'top_movies')
    xbmcplugin.endOfDirectory(plugin.handle)


TYPE_MOVIE = 'movie'
TYPE_SEASONS = 'seasons'
TYPE_EPISODE = 'episode'
TYPE_EPISODES = 'episodes'
TYPE_LANGUAGES = 'langs'
TYPE_PLAY = 'play'


def loadLanguages(movieId, tvShow):
    try:
        scriptUrl = 'Movie/main?id=' + movieId + '&js=1'

        if tvShow == 'True':
            scriptUrl = scriptUrl + '&serie=1'
            mode = TYPE_SEASONS
        else:
            mode = TYPE_MOVIE

        htmlData = utils.getResponse(scriptUrl)
        match = re.search(langsRegex, htmlData)
        langs = match.group(1).split(',')

        if mode == TYPE_MOVIE:
            match = re.search(qualityRegex, htmlData)
            quality = max([int(x) for x in match.group(1).split(',')])
            match = re.search(urlRegex, htmlData)
            url = match.group(1)
            info = utils.getInfo(BeautifulSoup(htmlData))

        for lang in langs:
            url = plugin.buildUrl({'mode': mode, 'id': movieId, 'lang': lang})
            li = utils.listItem(movieId, lang)
            if mode == TYPE_MOVIE:
                path = match.group(1).replace(
                    '{lang}', lang).replace('{quality}', str(quality))
                li.setInfo('video', {
                    'title': info['showTitle'],
                    'imdbnumber': info['imdbNumber'],
                })
                li.setContentLookup(False)
                #li.setProperty('IsPlayable', 'True')
                url = plugin.buildUrl({
                    'mode': TYPE_PLAY,
                    'url': path,
                    'title': info['showTitle'],
                    'imdbnumber': info['imdbNumber']
                })
                xbmcplugin.addDirectoryItem(
                    handle=plugin.handle, url=url, listitem=li, isFolder=False)
            else:
                xbmcplugin.addDirectoryItem(
                    handle=plugin.handle, url=url, listitem=li, isFolder=True)

    except Exception, e:
        plugin.log('error loading languages %s' % (str(e),))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)


def playItem(path, season=None, episode=None, title=None, tvShowTitle=None, imdbNumber=None):
    item = xbmcgui.ListItem(path=path)
    info = {
        'episode': episode,
        'season': season,
        'tvshowtitle': tvShowTitle,
        'showtitle': tvShowTitle,
        'showlink': tvShowTitle,
        'tvshowid': imdbNumber,
        'title': title,
        'imdbnumber': imdbNumber,
    }
    plugin.log("ADJNET: "+str(info))
    if not season is None:
        info['type'] = 'episode'
        info['mediatype'] = 'episode'
    else:
        info['type'] = 'movie'
        info['mediatype'] = 'movie'

    item.setInfo('video', info)
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=item)


def search():
    kb = xbmc.Keyboard('', 'Search for Movies')
    kb.doModal()
    if (kb.isConfirmed()):
        searchTerm = kb.getText()
    else:
        return

    searchUrl = 'search-advanced?movie_filters%5Bwith_actors%5D=3&movie_filters%5Bwith_directors%5D=1&movie_filters%5Bkeyword%5D=_&movie_filters%5Byear_range%5D=1900%2C2019&movie_filters%5Binit%5D=true&filters%5Btype%5D=movie&keywords=' + \
        searchTerm + '&page=1&per_page=20&source=adjaranet'
        
    try:
        data = utils.getJsonObject(searchUrl)
        for item in data['data']:
            movieId = item['adjaraId']
            url = plugin.buildUrl(
                {'mode': TYPE_LANGUAGES, 'id': movieId, 'tv_show': item['isTvShow']})
            li = utils.listItem(movieId, item['secondaryName'])
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)
    except Exception, e:
        plugin.log('error searching for %s \n %s' % (searchTerm, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)
