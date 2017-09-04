#!/usr/bin/env python3

from xl import player, event, providers, settings #common, 

from xlgui.widgets import menu, menuitems

import urllib, webbrowser

DATA = [
    # default value if can't read from 'settings.ini' [plugin/testing/search]
    ['Google.com', 'https://www.google.com/search?q=%s'],
    ['YouTube.com', 'https://www.youtube.com/results?search_query=%s'],
    ['Vimeo.com', 'https://vimeo.com/search?q=%s'],
    ['Vimeo.com [category: music]', 'https://vimeo.com/search?category=music&q=%s'],
    ['SoundCloud.com', 'https://soundcloud.com/search?q=%s'],
]

class Testing(object):
    
    def display(self, name, player, track=None):
        print '---------------------------------'
        print 'TESTING: display(name, player, track)'
        print 'TESTING: ------------------------'
        print 'TESTING:     name:', name
        print 'TESTING:   player:', player
        print 'TESTING:    track:', track
        print 'TESTING: ------------------------'
        print 'TESTING: player.current:', player.current
        
        if track:
            print 'TESTING: track.list_tags():', track.list_tags()
            print 'TESTING: track:', track
            for tag in ('title', 'album', 'artist', 'tracknumber', '__loc', '__basename'):
                data = track.get_tag_display(tag)
                print 'TESTING: tag: %11s =' % tag, data

        print '---------------------------------'
        
    def other(self, name):
        global DATA
        print 'TESTING: other(name)'
        print 'TESTING: ------------------------'
        print 'TESTING:     name:', name
        print 'TESTING: ------------------------'
        print "TESTING: settings.get_option('plugin/testing/search'):", settings.get_option('plugin/testing/search', DEFAULT_DATA)
        DATA = settings.set_option('plugin/testing/search', DEFAULT_DATA)
        print 'TESTING: ------------------------'

    # -----------------------------------------------------------------
    
    def enable(self, exaile):
        self.player = player.PLAYER
        
        self.display('enable', player.PLAYER)
        self.other('enable')

        event.add_callback(self.on_playback_start, 'playback_track_start')

    def disable(self, exaile):
        self.display('disable', player.PLAYER)
        self.other('disable')

    def teardown(self, exaile):
        self.display('teardown', player.PLAYER)
        self.other('teardown')

        event.remove_callback(self.on_playback_start, 'playback_track_start')

    def on_gui_loaded(self):
        self.display('on_gui_loaded', player.PLAYER)
        self.other('on_gui_loaded')

        ### main menu / tools ###
        
        self.menu = menu.simple_menu_item('furas', '', 'Get Current Track',
                                          callback=self.on_view_menu)
        #providers.register('menubar-tools-menu', self.menu)
        self.menu.register('menubar-tools-menu')
        
        ### menu 

        #self.create_test_menu()
        
        self.create_menu()
        
        #print 'TESTING: register menu'
        
    def item_register(self, item, menu):
        print '---------------------------------'
        print 'TESTING: item.register(', menu, ')'
        print '---------------------------------'
        item.register(menu)
        
    def provider_register(self, item, menu):
        print '---------------------------------'
        print 'TESTING: provider.register(', menu, ')'
        print '---------------------------------'
        providers.register(menu, item)
        
    def test_callback(self, window, name, parent, context):
        print '---------------------------------'
        print 'TESTING: test_callback(window, name, parent, context)'
        print 'TESTING: ------------------------'
        print 'TESTING:    window:', window
        print 'TESTING:      name:', name
        print 'TESTING:    parent:', parent
        print 'TESTING:   context:', context
        print 'TESTING: ------------------------'
        print 'TESTING: dir(parent):'
        for x in dir(parent):
            print 'TESTING:  ->', x
        
        print 'TESTING: ------------------------'
        print 'TESTING: items:'
        for item in parent.get_selected_items():
            print 'TESTING:  -> item:', item
            print 'TESTING:  -> type(item):', type(item)
            print 'TESTING:  -----'
            
        print 'TESTING: ------------------------'
        print 'TESTING: paths:' 
        for path in parent.get_selected_paths():
            print 'TESTING:  -> path:', path
            print 'TESTING:  -> type(path):', type(path)
            print 'TESTING:  -----'

        print 'TESTING: ------------------------'
        print 'tracks:', parent.get_selected_tracks()
        for track in parent.get_selected_tracks():
            print track
            print type(track)
            #print dir(track)
            print '-------------------'
            for tag in ('title', 'album', 'artist', 'tracknumber', '__loc', '__basename'):
                data = track.get_tag_display(tag)
                print ': %11s:' % tag, data
            print '-------------------'
            title = track.get_tag_display('title')
            webbrowser.open('http://www.wrzuta.pl/szukaj/%s' % title.replace(' ', '+'))
            webbrowser.open('https://www.google.pl/search?q=%s' % title.replace(' ', '+'))

        self.display('test_callback', player.PLAYER)
        
        with open('tracks.txt', 'a') as f:
            for track in parent.get_selected_tracks():
                artist = track.get_tag_display('artist')
                title = track.get_tag_display('title')
                f.write('%s,%s\n' % (artist,  title))
        print '---------------------------------'
        
    ### main menu / tools ###
        
    def on_view_menu(self, widget, name, parent, context):
        print '---------------------------------'
        print 'TESTING: on_view_menu(widget, name, parent, context)'
        print 'TESTING: ------------------------'
        #~ if self.window:
            #~ self.window.present()
        #~ else:
            #~ self.window = DeveloperWindow(self.exaile.gui.main.window, self)

            #~ def _delete(w, e):
                #~ self.window = None

            #~ self.window.connect('delete-event', _delete)
            #~ self.window.show_all()
        print '---------------------------------'

    def on_exaile_loaded(self):
        self.display('on_exaile_loaded', player.PLAYER)
        self.other('on_exaile_loaded')
    
    def on_playback_start(self, type, player, track):
        self.display('on_playback_start', player, track)
        self.other('on_playback_start')

    ### menu ###
    
    def create_test_menu(self):
        
        self.item = menu.simple_menu_item('furas-item', # name
            ['properties'], # after ie. [] or ['properties']
            'Testowy', # display text
            'gtk-save', # icon name # ie. 'document-properties'
            self.test_callback, # callback function
            callback_args=[] # callback extra arguments
        )
                
        #self.item_register(self.item, 'track-panel-menu')
        #self.item_register(self.item, 'playlist-panel-menu')
        #self.item_register(self.item, 'playlist-panel-context-menu')
        #self.item_register(self.item, 'collection-panel-context-menu')
        #self.item_register(self.item, 'files-panel-context-menu')
        #self.item_register(self.item, 'radio-panel-menu')
        
        #providers.register('menubar-file-menu', item)
        #providers.register('menubar-edit-menu', item)
        #providers.register('menubar-playlist-menu', item)
        #providers.register('menubar-playlist-menu', item)
        #providers.register('menubar-tools-menu', item)
        #providers.register('menubar-help-menu', item)
        
        #self.item.register('main-panel')        

        self.provider_register(self.item, 'playlist-context-menu')
        #self.item_register(self.item, 'playlist-context-menu')
        #self.item_register(self.item, 'playlist-columns-menu')

    def create_menu(self):

        sep = menu.simple_separator('furas-item-sep', ['properties'])
        #sep._pos = 'normal'
        self.provider_register(sep, 'playlist-context-menu')

        for n, (name, url) in enumerate(DATA):
            item = menu.simple_menu_item(
                'furas-item-%i' % n, # unique name
                ['furas-item-sep'], # after ie. [] or ['properties']
                name, # displayed text
                'gtk-save', # icon name # ie. 'document-properties'
                self.webbrowser_cb, # callback function
                callback_args=[url] # callback extra arguments
            )
            #print(dir(item))
            self.provider_register(item, 'playlist-context-menu')

        print '---------------------------------'
        print 'TESTING: register menu #1'
        
        ### submenu ###

        
        self.submenu = menu.Menu(self, inherit_context=True)
        
        for n, (name, url) in enumerate(DATA):
            self.submenu.add_item(menu.simple_menu_item(
                'furas-item-sub-%i' % n, # unique name
                [], # after ie. [] or ['properties']
                name, # displayed text
                'gtk-save', # icon name # ie. 'document-properties'
                self.webbrowser_cb, # callback function
                callback_args=[url] # callback extra arguments
            ))

        item = menu.simple_menu_item(
                'furas-item-sub', # unique name
                ['furas-item-sep'], # after ie. [] or ['properties']
                'Szukaj',
                submenu=self.submenu)
        
        self.provider_register(item, 'playlist-context-menu')
                
                
        print 'TESTING: self.submenu._items:'
        print self.submenu._items
        print '---------------------------------'
        print 'TESTING: register menu #2'

        for p in providers.get('playlist-context-menu'):
            print 'TESTING:  -> menu:', p.name, p._pos, p.after
        print '---------------------------------'
        

    def webbrowser_cb(self, window, name, parent, context, url):
        print '---------------------------------'
        print 'TESTING: webbrowser_cb(window, name, parent, context, url)'
        print 'TESTING: ------------------------'
        print 'TESTING:   window:', window
        print 'TESTING:     name:', name
        print 'TESTING:   parent:', parent
        print 'TESTING:  context:', context
        print 'TESTING:      url:', url
        print 'TESTING: ------------------------'
        
        for track in parent.get_selected_tracks():
            title = track.get_tag_display('title')
            print 'TESTING: selected_track:', title
            title = urllib.quote_plus(title)
            webbrowser.open(url % title)
        print '---------------------------------'
    
plugin_class = Testing

### events

#~ def enable(exaile):
    #~ event.add_callback(on_stop_action, 'quit_application')
    #~ event.add_callback(on_stop_action, 'playback_player_end', player.PLAYER)
    #~ event.add_callback(on_begin_action, 'playback_track_start', player.PLAYER)
    #~ event.add_callback(on_pause_action, 'playback_toggle_pause', player.PLAYER)
    
#~ def disable(exaile):
    #~ event.remove_callback(on_stop_action, 'quit_application')
    #~ event.remove_callback(on_stop_action, 'playback_player_end', player.PLAYER)
    #~ event.remove_callback(on_begin_action, 'playback_track_start', player.PLAYER)
    #~ event.remove_callback(on_pause_action, 'playback_toggle_pause', player.PLAYER)

### xlgui/panel/menus.py

#~ from xlgui.widgets import (
    #~ menu,
    #~ menuitems
#~ )

### Generic track selection menus


#~ def __create_track_panel_menus():

    #~ items = []

    #~ items.append(menuitems.EnqueueMenuItem('enqueue', after=['top-sep']))

    #~ items.append(menuitems.AppendMenuItem('append', after=[items[-1].name]))
    #~ items.append(menuitems.ReplaceCurrentMenuItem('replace', after=[items[-1].name]))
    #~ items.append(menuitems.RatingMenuItem('rating', after=[items[-1].name]))

    #~ items.append(menu.simple_separator('tp-sep', after=[items[-1].name]))

    #~ items.append(menuitems.PropertiesMenuItem('properties', after=[items[-1].name]))

    #~ for item in items:
        #~ item.register('track-panel-menu')


#~ __create_track_panel_menus()


#~ class TrackPanelMenu(menu.ProviderMenu):
    #~ '''
        #~ Context menu when a track is clicked on a panel
        #~ Provider key: track-panel-menu


### xlgui/widgets/menuitems.py

#~ def _properties_cb(widget, name, parent, context, get_tracks_func, dialog_parent):
    #~ tracks = get_tracks_func(parent, context)
    #~ if tracks:
        #~ properties.TrackPropertiesDialog(dialog_parent, tracks)


#~ def PropertiesMenuItem(name, after, get_tracks_func=generic_get_tracks_func,
                       #~ dialog_parent=None):
    #~ return menu.simple_menu_item(name, after, _("_Track Properties"),
                                 #~ 'document-properties', _properties_cb,
                                 #~ callback_args=[get_tracks_func, dialog_parent])
