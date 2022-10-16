import os
import os.path

from httpcore import stream
from platformcommon import PlatformCommon

class Platform_Pcengine(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']

        if emulator == 'retroarch':
            if core == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']

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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing extensions: " + str(extensions))
        print("\tUsing fullscreen: " + str(fullscreen))
        print("\tUsing recording: " + str(recording))
        print("\tUsing streaming: " + str(streaming))

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
                
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files

class Platform_Supergrafx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        
        if emulator == 'retroarch':
            if core == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']
        
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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing extensions: " + str(extensions))
        print("\tUsing fullscreen: " + str(fullscreen))
        print("\tUsing recording: " + str(recording))
        print("\tUsing streaming: " + str(streaming))

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
        
        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']
                
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files

class Platform_Pc8000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.

    emulators = ['retroarch']
    cores = ['quasi88_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['quasi88_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['d88', 'u88', 'm3u']
        
        if emulator == 'retroarch':
            if core == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']
                
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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing extensions: " + str(extensions))
        print("\tUsing fullscreen: " + str(fullscreen))
        print("\tUsing recording: " + str(recording))
        print("\tUsing streaming: " + str(streaming))

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
                
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc8000', 'pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files

class Platform_Pc8800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['quasi88_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['d88', 'u88', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['quasi88_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['d88', 'u88', 'm3u']

        if emulator == 'retroarch':
            if core == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']
                        
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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing extensions: " + str(extensions))
        print("\tUsing fullscreen: " + str(fullscreen))
        print("\tUsing recording: " + str(recording))
        print("\tUsing streaming: " + str(streaming))

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
                
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']
                        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files

class Platform_Pc98(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['nekop2_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['nekop2_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']
        
        if emulator == 'retroarch':
            if core == 'nekop2_libretro':
                extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']

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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc-98']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'nekop2_libretro':
                extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files

class Platform_Pcfx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['mednafen_pcfx_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['cue', 'ccd', 'toc', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_pcfx_libretro']
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['cue', 'ccd', 'toc', 'chd']
        
        if emulator == 'retroarch':
            if core == 'mednafen_pcfx_libretro':
                extensions = ['cue', 'ccd', 'toc', 'chd']

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
            # Set wether we should start recording or not.
            if recording != ['false']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
            # Set wether we should run in fullscreen or not.
            if fullscreen != ['false']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing extensions: " + str(extensions))
        print("\tUsing fullscreen: " + str(fullscreen))
        print("\tUsing recording: " + str(recording))
        print("\tUsing streaming: " + str(streaming))

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
                
        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)
    
    def supported_platforms(self):
        return ['pcfx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_pcfx_libretro':
                extensions = ['cue', 'ccd', 'toc', 'chd']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        ext_files.append(file)
                        print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        print("\tFound file: " + file)
        return ext_files