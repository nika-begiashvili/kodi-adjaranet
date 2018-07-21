from lib import plugin
import xbmcgui
import xbmcplugin

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