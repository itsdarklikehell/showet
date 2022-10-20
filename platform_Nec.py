import os
import os.path
import stat
import inquirer

from platformcommon import PlatformCommon

debugging = False
interactive = False

class Platform_Pcengine(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Supergrafx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro', 'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'mednafen_supergrafx_libretro':
                extensions = ['pce', 'sgx', 'cue', 'ccd', 'chd']
                
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Pc8000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['quasi88_libretro']
    extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['quasi88_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['quasi88_libretro']
        extensions = ['d88', 'u88', 'm3u']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc8000', 'pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Pc8800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['quasi88_libretro']
    extensions = ['d88', 'u88', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['quasi88_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['quasi88_libretro']
        extensions = ['d88', 'u88', 'm3u']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator == 'retroarch':
            if core == 'quasi88_libretro':
                extensions = ['d88', 'u88', 'm3u']
                        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Pc98(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['nekop2_libretro']
    extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['nekop2_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['nekop2_libretro']
        extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['pc-98']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator == 'retroarch':
            if core == 'nekop2_libretro':
                extensions = ['d98', 'zip', '98d', 'fdi', 'fdd', '2hd', 'tfd', 'd88', '88d', 'hdm', 'xdf', 'dup', 'cmd', 'hdi', 'thd', 'nhd', 'hdd']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Pcfx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mednafen_pcfx_libretro']
    extensions = ['cue', 'ccd', 'toc', 'chd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_pcfx_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['mednafen_pcfx_libretro']
        extensions = ['cue', 'ccd', 'toc', 'chd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            if interactive != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(emulators[0]))
                emulator = emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            if interactive != False:
                PlatformCommon.multicore(self,cores)
            else:
                if debugging != False:
                    print('interactive mode is off, using default' + str(cores[0]))
                core = cores[0]

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
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core)


        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            print("Using: " + str(emulator))

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))


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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)
    
    def supported_platforms(self):
        return ['pcfx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator == 'retroarch':
            if core == 'mednafen_pcfx_libretro':
                extensions = ['cue', 'ccd', 'toc', 'chd']

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                            print("\tMaking it executable for you")                        
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files