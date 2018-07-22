from lib import utils,plugin
import xbmcplugin
import xbmcgui

TYPE_MOVIE = 'movie'
TYPE_SEASONS = 'seasons'
TYPE_EPISODE = 'episode'
TYPE_EPISODES = 'episodes'
TYPE_LANGUAGES = 'langs'

def loadSeasons(movieId, lang):
    scriptUrl = 'Movie/main?id=' + movieId + '&serie=1&js=1'
    try:
        soup = utils.getHtml(scriptUrl)
        seasons = soup.find('div', {"class": "scrollB"})
        for span in seasons.findAll('span'):
            season = span.get('data-season')
            url = plugin.buildUrl({'mode': TYPE_EPISODES, 'id': movieId, 'season': season, 'lang': lang})
            li = utils.listItem(movieId,'Season ' + season)
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)

    except Exception, e:
        plugin.log('error loading seasons %s \n %s' %
                 (scriptUrl, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)


def loadEpisodes(movieId, lang, season):
    scriptUrl = 'Movie/main?id=' + movieId + '&serie=1&js=1'
    try:
        soup = utils.getHtml( scriptUrl )
        episodes = soup.findAll('span', {"data-season": str(season)})
        del episodes[0]
        for episode in episodes:
            langs = episode.findAll('div')
            for l in langs:
                if lang in str(l):
                    path = l.get('data-href')
                    break

            url = plugin.buildUrl({'mode': TYPE_EPISODE, 'url': path})
            li = utils.listItem(movieId,episode.contents[0],True)
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=False)

    except Exception, e:
        plugin.log('error loading episodes %s \n %s' %
                 (scriptUrl, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)

def loadEpisode(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)