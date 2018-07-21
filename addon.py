import simplejson as json
from httplib2 import Http
from BeautifulSoup import BeautifulSoup
import re
import urllib2
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
from lib import plugin,utils,common,movies

TYPE_MOVIE = 'movie'
TYPE_SEASONS = 'seasons'
TYPE_EPISODE = 'episode'
TYPE_EPISODES = 'episodes'
TYPE_LANGUAGES = 'langs'

find_var_regex = re.compile(r"""movieUrlEmpty\s*=\s*[\'\"](.+)[\'\"]""")
langs_regex = re.compile(r"""movieLangs\s*=\s*[\'\"](.+)[\'\"]""")
qualities_regex = re.compile(r"""movieQuals\s*=\s*[\'\"](.+)[\'\"]""")

plugin.setContent('movies')

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

def load_movie(movieId, lang):
    scriptUrl = 'Movie/main?id=' + movieId + '&js=1'
    try:
        htmlData = utils.getResponse(scriptUrl)
        match = re.search(find_var_regex, htmlData)
        if not match:
            plugin.log('can not find url at %s' % (scriptUrl,))
            raise Exception('url not found')

        maxQuality = re.search(qualities_regex, htmlData).group(1).split(',')[0]

        url = match.group(1).replace('{lang}', lang).replace('{quality}', maxQuality)
        
        play_item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)
    except Exception, e:
        xbmc.log('adjaranet: got http error fetching %s \n %s' %
                 (scriptUrl, str(e)), xbmc.LOGWARNING)

def load_languages(movieId, tvShow):
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
            li = build_kodi_list_item(mode, utils.getIcon('movie_id'), lang)
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=(mode == TYPE_SEASONS))

    except Exception, e:
        plugin.log('error loading languages %s' % (str(e),) )
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)


def load_seasons(movieId, lang):
    scriptUrl = 'Movie/main?id=' + movieId + '&serie=1&js=1'
    try:
        soup = utils.getHtml(scriptUrl)
        seasons = soup.find('div', {"class": "scrollB"})
        for span in seasons.findAll('span'):
            season = span.get('data-season')
            url = plugin.buildUrl(
                {'mode': TYPE_EPISODES, 'id': movieId, 'season': season, 'lang': lang})
            li = build_kodi_list_item(get_movie_type(
                3), utils.getCover('movie_id'), 'Season ' + season)
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=True)

    except Exception, e:
        plugin.log('error loading seasons %s \n %s' %
                 (scriptUrl, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)


def load_episodes(movieId, lang, season):
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
            li = xbmcgui.ListItem(episode.contents[0])
            li.setProperty('IsPlayable', 'True')
            xbmcplugin.addDirectoryItem(
                handle=plugin.handle, url=url, listitem=li, isFolder=False)

    except Exception, e:
        plugin.log('error loading episodes %s \n %s' %
                 (scriptUrl, str(e)))
    finally:
        xbmcplugin.endOfDirectory(plugin.handle)

def load_episode(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)

mode = plugin.args.get('mode', None)

if mode is None:
    common.mainScreen()
elif mode[0] == 'category':
    category = plugin.args.get('category', 'new_release')
    movies.loadCategory(category[0])
elif mode[0] == 'search':
    common.search()
elif mode[0] == TYPE_LANGUAGES:
    load_languages(plugin.args.get('id', None)[0], plugin.args.get('tv_show', None)[0])
elif mode[0] == TYPE_MOVIE:
    movie_id = plugin.args.get('id', None)
    load_movie(movie_id[0], plugin.args.get('lang', None)[0])
elif mode[0] == TYPE_SEASONS:
    movie_id = plugin.args.get('id', None)
    load_seasons(movie_id[0], plugin.args.get('lang', None)[0])
elif mode[0] == TYPE_EPISODES:
    movie_id = plugin.args.get('id', None)
    load_episodes(movie_id[0], plugin.args.get('lang', None)
                  [0], plugin.args.get('season', None)[0])
elif mode[0] == TYPE_EPISODE:
    load_episode(plugin.args.get('url', None)[0])
