import os
import os.path
import inquirer

from platformcommon import PlatformCommon

interactive = True
debugging = True

class Platform_3DS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'citra']
    cores = ['citra_libretro', 'citra2018_libretro', 'citra_canary_libretro', 'melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['3ds', '3dsx', 'elf', 'axf', 'cci', 'cxi', 'app']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['citra_libretro']
        emulators = ['retroarch', 'citra']
        cores = ['citra_libretro', 'citra2018_libretro', 'citra_canary_libretro', 'melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['3ds', '3dsx', 'elf', 'axf', 'cci', 'cxi', 'app']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)
        
        if emulator[0] == 'retroarch':
            if core[0] == 'citra_libretro' or core[0] == 'citra2018_libretro' or core[0] == 'citra_canary_libretro':
                extensions = ['3ds', '3dsx', 'elf', 'axf', 'cci', 'cxi', 'app']
        
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
        return ['nintendods']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator[0] == 'retroarch':
            if core[0] == 'citra_libretro' or core[0] == 'citra2018_libretro' or core[0] == 'citra_canary_libretro':
                extensions = ['3ds', '3dsx', 'elf', 'axf', 'cci', 'cxi', 'app']
        
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

class Platform_N64(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'mupen64plus-glide64', 'mupen64plus-glide64-lle', 'mupen64plus-gliden64']
    cores = ['mupen64plus_libretro', 'mupen64plus_next_libretro', 'parallel_n46_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['mupen64plus_next_libretro']
        emulators = ['retroarch', 'mupen64plus-glide64', 'mupen64plus-glide64-lle', 'mupen64plus-gliden64']
        cores = ['mupen64plus_libretro', 'mupen64plus_next_libretro', 'parallel_n46_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'mupen64plus_next_libretro':
                extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
                
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
        return ['nintendo64']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mupen64plus_next_libretro':
                extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
        
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

class Platform_DS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'desmume', 'melonds']
    cores = ['melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'nds', 'dsi']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['desmume_libretro']
        emulators = ['retroarch', 'desmume', 'melonds']
        cores = ['melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'nds', 'dsi']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'desmume_libretro':
                extensions = ['nds', 'dsi']
        
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
        return ['nintendods']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'desmume_libretro':
                extensions = ['nds', 'dsi']
                        
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

class Platform_Famicom(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
    cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro', 'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'nes', 'fds', 'unf', 'unif', 'qd', 'nsf']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['fceumm_libretro']
        emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
        cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro', 'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'nes', 'fds', 'unf', 'unif', 'qd', 'nsf']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)
        
        if emulator[0] == 'retroarch':
            if core[0] == 'quicknes_libretro' or core[0] == 'bnes_libretro':
                extensions = ['nes']
            if core[0] == 'emux_nes_libretro':
                extensions = ['nes', 'bin', 'rom']
            if core[0] == 'nestopia_libretro' or core[0] == 'fceumm_libretro' or core[0] == 'mesen_libretro':
                extensions = ['fds', 'nes', 'unif', 'unf']
                
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
        return ['nesfamicom']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'quicknes_libretro' or core[0] == 'bnes_libretro':
                extensions = ['nes']
            if core[0] == 'emux_nes_libretro':
                extensions = ['nes', 'bin', 'rom']
            if core[0] == 'nestopia_libretro' or core[0] == 'fceumm_libretro' or core[0] == 'mesen_libretro':
                extensions = ['fds', 'nes', 'unif', 'unf']
        
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

class Platform_FamicomDisksystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
    cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro', 'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'nes', 'fds', 'unf', 'unif', 'qd', 'nsf']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['quicknes_libretro']
        emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
        cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro', 'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']

        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'nes', 'fds', 'unf', 'unif', 'qd', 'nsf']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)
        
        if emulator[0] == 'retroarch':
            if core[0] == 'quicknes_libretro' or core[0] == 'bnes_libretro':
                extensions = ['nes']
            if core[0] == 'emux_nes_libretro':
                extensions = ['nes', 'bin', 'rom']
            if core[0] == 'nestopia_libretro' or core[0] == 'fceumm_libretro' or core[0] == 'mesen_libretro':
                extensions = ['fds', 'nes', 'unif', 'unf']

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
        return ['nesfamicom']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'quicknes_libretro' or core[0] == 'bnes_libretro':
                extensions = ['nes']
            if core[0] == 'emux_nes_libretro':
                extensions = ['nes', 'bin', 'rom']
            if core[0] == 'nestopia_libretro' or core[0] == 'fceumm_libretro' or core[0] == 'mesen_libretro':
                extensions = ['fds', 'nes', 'unif', 'unf']
        
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

class Platform_Gameboy(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['gambatte_libretro', 'mess2016_libretro', 'mess_libretro', 'mgba_libretro', 'tgbdual_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'gb', 'dmg', 'bin', 'u1', 'ndd', 'zip']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mesen-s_libretro']
        emulators = ['retroarch']
        cores = ['gambatte_libretro', 'mess2016_libretro', 'mess_libretro', 'mgba_libretro', 'tgbdual_libretro']

        streaming = ['false']
        recording = ['false']        
        extensions = ['zip', 'gb', 'dmg', 'bin', 'u1', 'ndd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            #gb/c
            if core[0] == 'emux_gb_libretro':
                extensions = ['gb', 'bin', 'rom']
            if core[0] == 'gambatte_libretro':
                extensions = ['gb', 'gbc', 'dmg']
            if core[0] == 'gearhub_libretro':
                extensions = ['gb', 'dmg', 'gbc', 'cgb', 'sgb']
            if core[0] == 'sameboy_libretro':
                extensions = ['gb', 'gbc']
            if core[0] == 'tgbdual_libretro':
                extensions = ['cgb', 'dmg', 'gb', 'gbc', 'sgb']                                                                
            #gba
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            #snes
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']

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
        return ['gameboy']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            #gb/c
            if core[0] == 'emux_gb_libretro':
                extensions = ['gb', 'bin', 'rom']
            if core[0] == 'gambatte_libretro':
                extensions = ['gb', 'gbc', 'dmg']
            if core[0] == 'gearhub_libretro':
                extensions = ['gb', 'dmg', 'gbc', 'cgb', 'sgb']
            if core[0] == 'sameboy_libretro':
                extensions = ['gb', 'gbc']
            if core[0] == 'tgbdual_libretro':
                extensions = ['cgb', 'dmg', 'gb', 'gbc', 'sgb']                                                                
            #gba
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            #snes
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
                            
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
class Platform_GameboyColor(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.    
    emulators = ['retroarch']
    cores = ['gambatte_libretro', 'mgba_libretro', 'tgbdual_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'gbc', 'dmg', 'bin', 'u1', 'ndd']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mesen-s_libretro']
        emulators = ['retroarch']
        cores = ['gambatte_libretro', 'mgba_libretro', 'tgbdual_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'gbc', 'dmg', 'bin', 'u1', 'ndd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)
        
        if emulator[0] == 'retroarch':
            #gb/c
            if core[0] == 'emux_gb_libretro':
                extensions = ['gb', 'bin', 'rom']
            if core[0] == 'gambatte_libretro':
                extensions = ['gb', 'gbc', 'dmg']
            if core[0] == 'gearhub_libretro':
                extensions = ['gb', 'dmg', 'gbc', 'cgb', 'sgb']
            if core[0] == 'sameboy_libretro':
                extensions = ['gb', 'gbc']
            if core[0] == 'tgbdual_libretro':
                extensions = ['cgb', 'dmg', 'gb', 'gbc', 'sgb']                                                                
            #gba
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            #snes
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
        
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
        return ['gameboy', 'gameboycolor']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            #gb/c
            if core[0] == 'emux_gb_libretro':
                extensions = ['gb', 'bin', 'rom']
            if core[0] == 'gambatte_libretro':
                extensions = ['gb', 'gbc', 'dmg']
            if core[0] == 'gearhub_libretro':
                extensions = ['gb', 'dmg', 'gbc', 'cgb', 'sgb']
            if core[0] == 'sameboy_libretro':
                extensions = ['gb', 'gbc']
            if core[0] == 'tgbdual_libretro':
                extensions = ['cgb', 'dmg', 'gb', 'gbc', 'sgb']                                                                
            #gba
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            #snes
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
        
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

class Platform_GameboyAdvance(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['meteor_libretro', 'vba_next_libretro', 'vbam_libretro', 'mgba_libretro', 'gpsp_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'gb', 'gbc', 'gba', 'dmg', 'agb', 'bin', 'cgb', 'sgb']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['vba_next_libretro']
        emulators = ['retroarch']
        cores = ['meteor_libretro', 'vba_next_libretro', 'vbam_libretro', 'mgba_libretro', 'gpsp_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'gb', 'gbc', 'gba', 'dmg', 'agb', 'bin', 'cgb', 'sgb']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            if core[0] == 'gpsp_libretro':
                extensions = ['gba', 'bin']
            if core[0] == 'meteor_libretro':
                extensions = ['gba']                
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'vbam_libretro':
                extensions = ['dmg', 'gb', 'gbc', 'cgb', 'sgb', 'gba']            
            if core[0] == 'vba_next_libretro':
                extensions = ['gba']
                
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
        return ['gameboyadvance', 'gameboycolor', 'gameboy']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_gba_libretro':
                extensions = ['gba', 'agb', 'bin']
            if core[0] == 'gpsp_libretro':
                extensions = ['gba', 'bin']
            if core[0] == 'meteor_libretro':
                extensions = ['gba']                
            if core[0] == 'mgba_libretro':
                extensions = ['gb', 'gbc', 'gba']
            if core[0] == 'tempgba_libretro':
                extensions = ['gba', 'bin', 'agb', 'gbz']
            if core[0] == 'vbam_libretro':
                extensions = ['dmg', 'gb', 'gbc', 'cgb', 'sgb', 'gba']            
            if core[0] == 'vba_next_libretro':
                extensions = ['gba']
                        
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

class Platform_Gamecube(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['dolphin_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['dolphin_libretro']
        emulators = ['retroarch']
        cores = ['dolphin_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'dolphin_libretro':
                extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']

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
        return ['gamecube']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'dolphin_libretro':
                extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        
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

class Platform_Pokemini(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['pokemini_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'min']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['pokemini_libretro']
        emulators = ['retroarch']
        cores = ['pokemini_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'min']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'pokemini_libretro':
                extensions = ['min']

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
        return ['pokemini']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'pokemini_libretro':
                extensions = ['min']
        
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

class Platform_SuperFamicom(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['snes9x_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'sfc', 'smc', 'fig', 'swc', 'bs']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['snes9x_libretro']     
        emulators = ['retroarch']
        cores = ['snes9x_libretro']
           
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'sfc', 'smc', 'fig', 'swc', 'bs']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'bsnes_libretro' or core[0] == 'bsnes_hd_beta_libretro' or core[0] == 'bsnes_cplusplus98_libretro' or core[0] == 'bsnes2014_accuracy_libretro' or core[0] == 'bsnes2014_balanced_libretro' or core[0] == 'bsnes2014_performance_libretro' or core[0] == 'bsnes_mercury_accuracy_libretro' or core[0] == 'bsnes_mercury_balanced_libretro' or core[0] == 'bsnes_mercury_balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bs']
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
            if core[0] == 'snes9x_libretro' or core[0] == 'snes9x2002_libretro' or core[0] == 'snes9x2005_libretro' or core[0] == 'snes9x2005_plus_libretro' or core[0] == 'snes9x2010_libretro':
                extensions = ['smc', 'sfc', 'swc', 'fig', 'bs', 'st']

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
        return ['snessuperfamicom']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'bsnes_libretro' or core[0] == 'bsnes_hd_beta_libretro' or core[0] == 'bsnes_cplusplus98_libretro' or core[0] == 'bsnes2014_accuracy_libretro' or core[0] == 'bsnes2014_balanced_libretro' or core[0] == 'bsnes2014_performance_libretro' or core[0] == 'bsnes_mercury_accuracy_libretro' or core[0] == 'bsnes_mercury_balanced_libretro' or core[0] == 'bsnes_mercury_balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bs']
            if core[0] == 'higan_sfc_libretro' or core[0] == 'higan_sfc balanced_libretro':
                extensions = ['sfc', 'smc', 'gb', 'gbc', 'bml', 'rom']
            if core[0] == 'mesen-s_libretro':
                extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
            if core[0] == 'snes9x_libretro' or core[0] == 'snes9x2002_libretro' or core[0] == 'snes9x2005_libretro' or core[0] == 'snes9x2005_plus_libretro' or core[0] == 'snes9x2010_libretro':
                extensions = ['smc', 'sfc', 'swc', 'fig', 'bs', 'st']
        
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

class Platform_Virtualboy(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['mednafen_vb_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'vb', 'vboy', 'bin']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_vb_libretro']
        emulators = ['retroarch']
        cores = ['mednafen_vb_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'vb', 'vboy', 'bin']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_vb_libretro':
                extensions = ['vb', 'vboy', 'bin']
                
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

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
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
        return ['virtualboy']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_vb_libretro':
                extensions = ['vb', 'vboy', 'bin']
                        
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

class Platform_Wii(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['dolphin_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['dolphin_libretro']
        emulators = ['retroarch']
        cores = ['dolphin_libretro']

        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator = self.multiemu(emulators)
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core = self.multicore(cores)

        if emulator[0] == 'retroarch':
            if core[0] == 'dolphin_libretro':
                extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        
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
        return ['wii', 'wiiu', 'nintendowii']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'dolphin_libretro':
                extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz', 'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        
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
