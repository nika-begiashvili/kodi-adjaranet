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
#elif mode[0] == TYPE_MOVIE:
#    load_movie( plugin.getArg('id') , plugin.getArg('lang','eng'))
elif mode[0] == TYPE_SEASONS:
    contentType = 'tvshows'
    movie_id = plugin.args.get('id', None)
    tv_shows.loadSeasons( plugin.getArg('id'), plugin.getArg('lang','eng'))
elif mode[0] == TYPE_EPISODES:
    contentType = 'episodes'
    movie_id = plugin.args.get('id', None)
    tv_shows.loadEpisodes(plugin.getArg('id'), plugin.getArg('lang','eng'), plugin.getArg('season'))
#elif mode[0] == TYPE_EPISODE:
#    tv_shows.loadEpisode( plugin.getArg('url') )

plugin.setContent(contentType)