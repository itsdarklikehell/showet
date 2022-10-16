import os
import os.path
from platformcommon import PlatformCommon

class Platform_32X(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'picodrive']
    cores = ['picodrive_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['picodrive_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
        
        if emulator == 'retroarch':
            if core == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
            
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['sega32x']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
        
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

class Platform_Dreamcast(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'flycast', 'redream']
    cores = ['flycast_libretro', 'flycast_gles2_libretro', 'retrodream_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['chd', 'cdi', 'elf', 'bin', 'cue', 'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['flycast_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['chd', 'cdi', 'elf', 'bin', 'cue', 'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
        
        if emulator == 'retroarch':
            if core == 'flycast_libretro' or core == 'flycast_gles2_libretro':
                extensions = ['chd', 'cdi', 'elf', 'bin', 'cue', 'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
            if core == 'retrodream_libretro':
                extensions = ['gdi', 'chd', 'cdi']

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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['dreamcast']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'flycast_libretro' or core[0] == 'flycast_gles2_libretro':
                extensions = ['chd', 'cdi', 'elf', 'bin', 'cue', 'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
            if core[0] == 'retrodream_libretro':
                extensions = ['gdi', 'chd', 'cdi']
                
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
class Platform_Gamegear(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    fullscreens = ['false']
    cores = ['gearsystem_libretro', 'genesis_plus_gx_libretro', 'fbneo_gg_libretro']
    streamings = ['twitch', 'youtube']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['genesis_plus_gx_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

        if emulator == 'retroarch':
            #MS/GG/MD/CD
            if core == 'genesis_plus_gx_libretro' or core == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/GG/SG-1000
            if core == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
                        
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
                
        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segagamegear']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            #MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
        
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

class Platform_Mastersystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    cores = ['genesis_plus_gx_libretro', 'fbneo_sms_libretro', 'gearsystem_libretro', 'picodrive_libretro', 'smsplus_gx_libreto']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['genesis_plus_gx_libretro']        
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        
        if emulator == 'retroarch':
            #MS
            if core == 'emux_sms_libretro':
                extensions = ['sms', 'bms', 'bin', 'rom']
            #MS/GG/MD/CD
            if core == 'genesis_plus_gx_libretro' or core == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/MD/CD/32X
            if core == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
            #MS/GG/SG-1000
            if core == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
            #MSX/SVI/ColecoVision/SG-1000
            if core == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
            
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segamastersystem', 'segagamegear', 'segasg1000', 'segagenesismegadrive', 'segasaturn', 'segastv']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            #MS
            if core[0] == 'emux_sms_libretro':
                extensions = ['sms', 'bms', 'bin', 'rom']
            #MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
            #MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
            #MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
                        
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

class Platform_Megadrive(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'dgen']
    cores = ['genesis_plus_gx_libretro', 'fbneo_md_libretro', 'picodrive_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['picodrive_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        
        if emulator == 'retroarch':
            #MS/GG/MD/CD
            if core == 'genesis_plus_gx_libretro' or core == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/MD/CD/32X
            if core == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segagenesismegadrive']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            #MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            #MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
        
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

class Platform_Saturn(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    fullscreens = ['false']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    streamings = ['twitch', 'youtube']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['yabause_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
        
        if emulator == 'retroarch':
            if core == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core == 'yabause_libretro' or core == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segasaturn']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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

class Platform_Stv(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['kronos_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']

        if emulator == 'retroarch':
            if core == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core == 'yabause_libretro' or core == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']
        
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segastv']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']
        
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

class Platform_Vmu(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'vemulator']
    cores = ['vemulator_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['zip', 'vms', 'dci', 'bin']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vemulator_libretro']
        streaming = ['twitch']
        extensions = ['zip', 'vms', 'dci', 'bin']
        
        if emulator == 'retroarch':
            if core == 'vemulator_libretro':
                extensions = ['vms', 'dci', 'bin']
        
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segavmu']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        
        if emulator[0] == 'retroarch':
            if core[0] == 'vemulator_libretro':
                extensions = ['vms', 'dci', 'bin']
                        
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

class Platform_SG1000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'gearsystem']
    cores = ['gearsystem_libretro', 'bluemsx_libretro']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube']
    recordings = ['true']
    extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['bluemsx_libretro']
        fullscreen = ['false']
        streaming = ['twitch']
        recording = ['true']
        extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

        if emulator == 'retroarch':
            #MSX/SVI/ColecoVision/SG-1000
            if core == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
        
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
            
            # Set whether we should start streaming to twitch or not.
            if streaming == ['twitch']:
                print("\tTwitch Streaming enabled!")
                emulator.append('-r rtmp://ams03.contribute.live-video.net/app/$YOUR_STREAM_KEY')

            # Set whether we should start streaming to youtube or not.
            if streaming == ['youtube']:
                print("\tYoutube Streaming enabled!")
                emulator.append('-r rtmp://a.rtmp.youtube.com/live2/$YOUR_STREAM_KEY')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                print("\tRecording enabled!")
                emulator.append('-P ~/.config/retroarch/records')
                emulator.append('-r ~/.config/retroarch/records')
                # emulator.append('--recordconfig twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
        print("\tUsing recording: " + str(recording[0]))
        print("\tUsing streaming: " + str(streaming[0]))

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
        return ['segasg1000']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            #MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
        
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
