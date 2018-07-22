import re
import xbmc
import xbmcgui
import xbmcplugin
from lib import plugin,utils,common,movies,tv_shows

TYPE_MOVIE = 'movie'
TYPE_SEASONS = 'seasons'
TYPE_EPISODE = 'episode'
TYPE_EPISODES = 'episodes'
TYPE_LANGUAGES = 'langs'

find_var_regex = re.compile(r"""movieUrlEmpty\s*=\s*[\'\"](.+)[\'\"]""")
langs_regex = re.compile(r"""movieLangs\s*=\s*[\'\"](.+)[\'\"]""")
qualities_regex = re.compile(r"""movieQuals\s*=\s*[\'\"](.+)[\'\"]""")

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
        plugin.log('adjaranet: got http error fetching %s \n %s' % (scriptUrl, str(e)))

mode = plugin.args.get('mode', None)

contentType = 'movies'

if mode is None:
    common.mainScreen()
elif mode[0] == 'category':
    movies.loadCategory( plugin.getArg('category','new_release') )
elif mode[0] == 'search':
    common.search()
elif mode[0] == TYPE_LANGUAGES:
    common.loadLanguages( plugin.getArg('id'), plugin.getArg('tv_show',False) )
elif mode[0] == TYPE_MOVIE:
    load_movie( plugin.getArg('id') , plugin.getArg('lang','eng'))
elif mode[0] == TYPE_SEASONS:
    contentType = 'tvshows'
    movie_id = plugin.args.get('id', None)
    tv_shows.loadSeasons( plugin.getArg('id'), plugin.getArg('lang','eng'))
elif mode[0] == TYPE_EPISODES:
    contentType = 'episodes'
    movie_id = plugin.args.get('id', None)
    tv_shows.loadEpisodes(plugin.getArg('id'), plugin.getArg('lang','eng'), plugin.getArg('season'))
elif mode[0] == TYPE_EPISODE:
    tv_shows.loadEpisode( plugin.getArg('url') )

plugin.setContent(contentType)