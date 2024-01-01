import xbmcgui
import xbmcaddon
import xbmcvfs
import xbmc
import shutil
import os
class HTProviderMenu:

    def __init__(self):
        self.addon = xbmcaddon.Addon()

    def show_dialog(self):
        script_providers_path = os.path.dirname(os.path.abspath(__file__)) + '/providers/'
        providers = os.listdir(script_providers_path)
        addon_data_providers_path = xbmcvfs.translatePath('special://userdata/addon_data/script.elementum.burst/providers/')
        options = []
        preselect = []

        for index, provider in enumerate(providers):
            options.append(provider)
            
            if os.path.exists(addon_data_providers_path + provider):
                preselect.append(index)
        
        dialog = xbmcgui.Dialog()
        result = dialog.multiselect("Select provider:", options, preselect=preselect)

        if not result is None:
            for index, provider in enumerate(providers):
                source_path = script_providers_path + provider
                dest_path = addon_data_providers_path + provider

                if os.path.exists(dest_path):
                    os.remove(dest_path) 

                if index in result:
                    shutil.copy2(source_path, dest_path)

                
            # xbmcgui.Dialog().ok(self.addon.getAddonInfo('name'), 'result')

if __name__ == '__main__':
    addon = HTProviderMenu()
    addon.show_dialog()