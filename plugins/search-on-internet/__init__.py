from xlgui.widgets import menu
import urllib, webbrowser

#
# SOI - Search On Internet
#

DATA = [
    ['Google.com', 'https://www.google.com/search?q=%s'],
    ['YouTube.com', 'https://www.youtube.com/results?search_query=%s'],
    ['Vimeo.com', 'https://vimeo.com/search?q=%s'],
    ['Vimeo.com [category: music]', 'https://vimeo.com/search?category=music&q=%s'],
    ['SoundCloud.com', 'https://soundcloud.com/search?q=%s'],
#    ['Wrzuta.pl', 'http://www.wrzuta.pl/szukaj/%s'],
#    ['Wrzuta.pl [category: music]', 'http://www.wrzuta.pl/szukaj/audio/%s'],
]

class SearchOnInternetPlugin(object):

    def enable(self, exaile):
        print 'SearchOnInternetPlugin : enable'

    #def disable(self, exaile):
    #    print 'SearchOnInternetPlugin : disable'
    #    self.teardown()

    #def teardown(self, exaile):
    #    print 'SearchOnInternetPlugin : teardown'

    #------------------------------------------------------------------

    def on_gui_loaded(self):
        print 'SearchOnInternetPlugin : on_gui_loaded'
        self.create_menu()

    #def on_exaile_loaded(self):
    #    print 'SearchOnInternetPlugin : on_exaile_loaded'

    #------------------------------------------------------------------

    def create_menu(self):
        print 'SearchOnInternetPlugin : create menu'

        # list of registered items - to unregister on exit/teardown
        self._items = []

        # create separator (after 'properties')
        sep = menu.simple_separator(
            'soi-sep',     # unique name/ID in menu
            ['properties'] # put after (ie. [] or ['properties'])
        )
        # add separator to menu
        sep.register('playlist-context-menu')
        # add separtor to list
        self._items.append(sep)

        for n, (name, url) in enumerate(DATA):
            # create item (after separator 'soi-sep')
            item = menu.simple_menu_item(
                'soi-%i' % n, # unique name/ID in menu
                ['soi-sep'],  # put after (ie. [] or ['properties'])
                'Search on %s' % name, # displayed text
                'gtk-save',   # icon name (ie. 'document-properties', 'applications-internet', 'edit-find')
                self.webbrowser_cb, # callback function name
                callback_args=[url] # callback extra arguments
            )
            # add item to menu
            item.register('playlist-context-menu')
            # add item to list
            self._items.append(item)

    # --- callbacks (cb) ---

    def webbrowser_cb(self, window, name, parent, context, url):

        for track in parent.get_selected_tracks():
            # get title
            title = track.get_tag_display('title')
            print 'SearchOnInternetPlugin : title:', title
            
            # convert special chars
            full_url = url % urllib.quote_plus(title)
            print 'SearchOnInternetPlugin :   url:', full_url
            
            # open in browser
            webbrowser.open(full_url)

plugin_class = SearchOnInternetPlugin
