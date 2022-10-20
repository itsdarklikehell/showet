import os
import os.path
iport stat
import inquirer

from platformcommon import PlatformCommon

interactive = True
debugging = True

class Platform_Psx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['pcsx_rearmed_libretro', 'mednafen_psx_libretro', 'swanstation_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['swanstation_libretro']
        emulators = ['retroarch', 'other']
        cores = ['pcsx_rearmed_libretro', 'mednafen_psx_libretro', 'swanstation_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

        # # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        # if len(emulators) > 1:
        #     if interactive != False:
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #     else:
        #         emulator = emulators[0]
        
        # # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        # if len(cores) > 1:
        #     if interactive != False:
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #     else:
        #         core = core[0]

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


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            print("Using: " + str(emulator))

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
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files


class Platform_Ps2(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['pcsx2_libretro', 'play_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['pcsx2_libretro']
        emulators = ['retroarch', 'other']
        cores = ['pcsx2_libretro', 'play_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img', 'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

        # # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        # if len(emulators) > 1:
        #     if interactive != False:
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #     else:
        #         emulator = emulators[0]
        
        # # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        # if len(cores) > 1:
        #     if interactive != False:
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #     else:
        #         core = core[0]

        if emulator[0] == 'retroarch':
            if core[0] == 'pcsx2_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img', 'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'play_libretro':
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


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
            print("Using: " + str(emulator))

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
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files


class Platform_Psp(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'ppsspp']
    cores = ['ppsspp_libretro']
    fullscreens = ['false']
    streamings = ['false', 'twitch', 'youtube', 'restream']
    recordings = ['true', 'false']
    extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['ppsspp_libretro']
        emulators = ['retroarch', 'ppsspp']
        cores = ['ppsspp_libretro']
        
        fullscreen = ['false']
        streaming = ['false']
        recording = ['false']
        extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

        # # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        # if len(emulators) > 1:
        #     if interactive != False:
        #         emulator = inquirer.prompt(prompt).get('emulators').strip().lower()
        #     else:
        #         emulator = emulators[0]
        
        # # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        # if len(cores) > 1:
        #     if interactive != False:
        #         core = inquirer.prompt(prompt).get('cores').strip().lower()
        #     else:
        #         core = core[0]

        if emulator[0] == 'retroarch':
            if core[0] == 'ppsspp_libretro':
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


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'ppsspp':
            print("Using: " + str(emulator))

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
                        if debugging != False:
                            print("\tFound file: " + file)
                    if file.endswith(ext.upper()):
                        ext_files.append(file)
                        if debugging != False:
                            print("\tFound file: " + file)
        return ext_files
