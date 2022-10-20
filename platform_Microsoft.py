import os
import os.path
import inquirer

from platformcommon import PlatformCommon

interactive = True
debugging = True

class Platform_Xbox(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['directxbox_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'iso']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['directxbox_libretro']
        emulators = ['retroarch']
        cores = ['directxbox_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'iso']

        # emulator = []
        # core = []
        # def multiman(emulators,cores):
        #     # If multiple emulators are specified (e.g. 'retroarch', 'vice') ask the user to specify which one to use.
        #     if len(emulators) > 1:
        #         print('Info: Multiple emulators are supported: ' + str(emulators))
        #         prompt = [
        #             inquirer.List('emulators', message='Please select one of the supported emulators to continue', choices=emulators),
        #         ]
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(emulator))
        #             #emulator = str(emulator)
        #     else:
        #         #emulator = emulators
        #         print('Info: Only 1 emulator is supported: ' + str(emulator))
        #     # If multiple cores are specified (e.g. 'vice_x64sc_libretro', 'frodo_libretro') ask the user to specify which one to use.
        #     if len(cores) > 1:
        #         print('Info: Multiple cores are supported: ' + str(cores))
        #         prompt = [
        #             inquirer.List('cores', message='Please select one of the supported emulators to continue', choices=cores),
        #         ]
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(core))
        #             #core = str(core)
        #     else:
        #         #core = cores
        #         print('Info: Only 1 core is supported: ' + str(core))

        # multiman(emulators,cores)
                
        if emulator[0] == 'retroarch':
            if core[0] == 'directxbox_libretro':
                extensions = ['iso']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])
            if streaming != ['false']:
                # Set whether we should start streaming to twitch or not.
                if streaming == ['twitch']:
                    print("\tTwitch Streaming enabled!")
                    emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to restream or not.
                if streaming == ['restream']:
                    print("\tRestream Streaming enabled!")
                    emulator.append('-r rtmp://live.restream.io/live/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to youtube or not.
                if streaming == ['youtube']:
                    print("\tYoutube Streaming enabled!")
                    emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            # Set whether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set whether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'directxbox':
            # Set whether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))
            print("\tUsing fullscreen: " + str(fullscreen))
            print("\tUsing recording: " + str(recording))
            print("\tUsing streaming: " + str(streaming))

        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            with open(flipfile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            
        self.run_process(emulator)

    def supported_platforms(self):
        return ['xbox']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'directxbox_libretro':
                extensions = ['iso']
                        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files

class Platform_Msx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'openmsx', 'openmsx-msx2', 'openmsx-msx2-plus', 'openmsx-msx-turbo']
    cores = ['bluemsx_libretro', 'fbneo_msx_libretro', 'fmsx_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['bluemsx_libretro']
        emulators = ['retroarch', 'openmsx', 'openmsx-msx2', 'openmsx-msx2-plus', 'openmsx-msx-turbo']
        cores = ['bluemsx_libretro', 'fbneo_msx_libretro', 'fmsx_libretro']

        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

        # emulator = []
        # core = []
        # def multiman(emulators,cores):
        #     # If multiple emulators are specified (e.g. 'retroarch', 'vice') ask the user to specify which one to use.
        #     if len(emulators) > 1:
        #         print('Info: Multiple emulators are supported: ' + str(emulators))
        #         prompt = [
        #             inquirer.List('emulators', message='Please select one of the supported emulators to continue', choices=emulators),
        #         ]
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(emulator))
        #             #emulator = str(emulator)
        #     else:
        #         #emulator = emulators
        #         print('Info: Only 1 emulator is supported: ' + str(emulator))
        #     # If multiple cores are specified (e.g. 'vice_x64sc_libretro', 'frodo_libretro') ask the user to specify which one to use.
        #     if len(cores) > 1:
        #         print('Info: Multiple cores are supported: ' + str(cores))
        #         prompt = [
        #             inquirer.List('cores', message='Please select one of the supported emulators to continue', choices=cores),
        #         ]
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(core))
        #             #core = str(core)
        #     else:
        #         #core = cores
        #         print('Info: Only 1 core is supported: ' + str(core))

        # multiman(emulators,cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
            if core[0] == 'fmsx_libretro':
                extensions = ['rom', 'mx1', 'mx2', 'dsk', 'fdi', 'cas', 'm3u']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])
            if streaming != ['false']:
                # Set whether we should start streaming to twitch or not.
                if streaming == ['twitch']:
                    print("\tTwitch Streaming enabled!")
                    emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to restream or not.
                if streaming == ['restream']:
                    print("\tRestream Streaming enabled!")
                    emulator.append('-r rtmp://live.restream.io/live/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to youtube or not.
                if streaming == ['youtube']:
                    print("\tYoutube Streaming enabled!")
                    emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            # Set whether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set whether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == '4do':
            if streaming != ['false']:
                # Set whether we should start streaming to twitch or not.
                if streaming == ['twitch']:
                    print("\tTwitch Streaming enabled!")
                    emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to restream or not.
                if streaming == ['restream']:
                    print("\tRestream Streaming enabled!")
                    emulator.append('-r rtmp://live.restream.io/live/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to youtube or not.
                if streaming == ['youtube']:
                    print("\tYoutube Streaming enabled!")
                    emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            # Set whether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set whether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))
            print("\tUsing fullscreen: " + str(fullscreen))
            print("\tUsing recording: " + str(recording))
            print("\tUsing streaming: " + str(streaming))

        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            with open(flipfile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['msx', 'msx2', 'msx2plus', 'msxturbor', 'spectravideo3x8']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
            if core[0] == 'fmsx_libretro':
                extensions = ['rom', 'mx1', 'mx2', 'dsk', 'fdi', 'cas', 'm3u']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files

class Platform_Windows(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['wine']
    cores = ['wine']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['exe']
    # wineprefix = self.showetdir + '/wineprefix'

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['wine']
        core = ['wine']
        emulators = ['wine']
        cores = ['wine']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['exe']
        wineprefix = self.showetdir + '/wineprefix'
        
        # emulator = []
        # core = []
        # def multiman(emulators,cores):
        #     # If multiple emulators are specified (e.g. 'retroarch', 'vice') ask the user to specify which one to use.
        #     if len(emulators) > 1:
        #         print('Info: Multiple emulators are supported: ' + str(emulators))
        #         prompt = [
        #             inquirer.List('emulators', message='Please select one of the supported emulators to continue', choices=emulators),
        #         ]
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(emulator))
        #             #emulator = str(emulator)
        #     else:
        #         #emulator = emulators
        #         print('Info: Only 1 emulator is supported: ' + str(emulator))
        #     # If multiple cores are specified (e.g. 'vice_x64sc_libretro', 'frodo_libretro') ask the user to specify which one to use.
        #     if len(cores) > 1:
        #         print('Info: Multiple cores are supported: ' + str(cores))
        #         prompt = [
        #             inquirer.List('cores', message='Please select one of the supported emulators to continue', choices=cores),
        #         ]
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #         if debugging != False:
        #             print('Info: You selected: ' + str(core))
        #             #core = str(core)
        #     else:
        #         #core = cores
        #         print('Info: Only 1 core is supported: ' + str(core))

        # multiman(emulators,cores)
        
        if emulator[0] == 'wine':
            if core[0] == 'wine':
                extensions = ['exe']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])
            if streaming != ['false']:
                # Set whether we should start streaming to twitch or not.
                if streaming == ['twitch']:
                    print("\tTwitch Streaming enabled!")
                    emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to restream or not.
                if streaming == ['restream']:
                    print("\tRestream Streaming enabled!")
                    emulator.append('-r rtmp://live.restream.io/live/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to youtube or not.
                if streaming == ['youtube']:
                    print("\tYoutube Streaming enabled!")
                    emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            # Set whether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set whether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here
        if emulator[0] == 'wine':
            if streaming != ['false']:
                # Set whether we should start streaming to twitch or not.
                if streaming == ['twitch']:
                    print("\tTwitch Streaming enabled!")
                    emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to restream or not.
                if streaming == ['restream']:
                    print("\tRestream Streaming enabled!")
                    emulator.append('-r rtmp://live.restream.io/live/$YOUR_STREAM_KEY')
                # Set whether we should start streaming to youtube or not.
                if streaming == ['youtube']:
                    print("\tYoutube Streaming enabled!")
                    emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            # Set whether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set whether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
            exefile = files[0]

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))
            print("\tUsing fullscreen: " + str(fullscreen))
            print("\tUsing recording: " + str(recording))
            print("\tUsing streaming: " + str(streaming))
            print("\tGuessed executable file: " + exefile)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed
        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win64" winecfg')
        self.run_process([emulator[0], exefile])

    def supported_platforms(self):
        return ['windows', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'wine':
            if core[0] == 'wine':
                extensions = ['exe']
                        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files