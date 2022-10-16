import os
import os.path
from platformcommon import PlatformCommon

class Platform_Psx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['pcsx_rearmed_libretro', 'mednafen_psx_libretro', 'swanstation_libretro']
    fullscreens = ['false']
    streaming = ['true']
    recording = ['false']
    extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['swanstation_libretro']
        fullscreen = ['false']
        streaming = ['true']
        recording = ['false']
        extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']
        
        if emulator == 'retroarch':
            if core == 'duckstation_libretro' or core == 'swanstation_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img', 'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core == 'rustation_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe']
            if core == 'mednafen_psx_libretro' or core == 'mednafen_psx_hw_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe', 'pbp', 'chd']
            if core == 'pcsx1_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf', 'pbp', 'toc', 'cbn', 'm3u']
            if core == 'pcsx_rearmed_libretro' or core == 'pcsx_rearmed_neon_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf', 'pbp', 'toc', 'cbn', 'm3u', 'ccd', 'chd']

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
            
            # Set wether we should start streaming or not.
            if streaming == ['true']:
                print("\tStreaming enabled!")
                recording = 'true'
                emulator.append('-r rtmp://live.twitch.tv/app/$YOUR_TWITCH_ID')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                emulator.append('-R ~/.config/retroarch/records')
                emulator.append('--recordconfig ~/.config/retroarch/records_config/twitch.cfg')
                
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
        return ['playstation']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'duckstation_libretro' or core[0] == 'swanstation_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img', 'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'rustation_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe']
            if core[0] == 'mednafen_psx_libretro' or core[0] == 'mednafen_psx_hw_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe', 'pbp', 'chd']
            if core[0] == 'pcsx1_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf', 'pbp', 'toc', 'cbn', 'm3u']
            if core[0] == 'pcsx_rearmed_libretro' or core[0] == 'pcsx_rearmed_neon_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf', 'pbp', 'toc', 'cbn', 'm3u', 'ccd', 'chd']
        
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


class Platform_Ps2(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['pcsx2_libretro', 'play_libretro']
    fullscreens = ['false']
    streaming = ['true']
    recording = ['false']
    extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['pcsx2_libretro']
        fullscreen = ['false']
        streaming = ['true']
        recording = ['false']
        extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

        if emulator == 'retroarch':
            if core == 'pcsx2_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img', 'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core == 'play_libretro':
                extensions = ['chd', 'cso', 'cue', 'elf', 'iso', 'isz']
        
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
            
            # Set wether we should start streaming or not.
            if streaming == ['true']:
                print("\tStreaming enabled!")
                recording = 'true'
                emulator.append('-r rtmp://live.twitch.tv/app/$YOUR_TWITCH_ID')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                emulator.append('-R ~/.config/retroarch/records')
                emulator.append('--recordconfig ~/.config/retroarch/records_config/twitch.cfg')
                
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
        return ['playstation2']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'pcsx2_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img', 'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'play_libretro':
                extensions = ['chd', 'cso', 'cue', 'elf', 'iso', 'isz']
        
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


class Platform_Psp(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'ppsspp']
    cores = ['ppsspp_libretro']
    fullscreens = ['false']
    streaming = ['true']
    recording = ['false']
    extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['ppsspp_libretro']
        fullscreen = ['false']
        streaming = ['true']
        recording = ['false']
        extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
        
        if emulator == 'retroarch':
            if core == 'ppsspp_libretro':
                extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

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
            
            # Set wether we should start streaming or not.
            if streaming == ['true']:
                print("\tStreaming enabled!")
                recording = 'true'
                emulator.append('-r rtmp://live.twitch.tv/app/$YOUR_TWITCH_ID')
            
            # Set wether we should start recording or not.
            if recording == ['true']:
                emulator.append('-R ~/.config/retroarch/records')
                emulator.append('--recordconfig ~/.config/retroarch/records_config/twitch.cfg')
                
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                print("\tFullscreen enabled!")
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'ppsspp':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))
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
            if emulator[0] == 'ppsspp':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstationportable']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'ppsspp_libretro':
                extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
        
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
