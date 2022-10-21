import os
import os.path
import stat
import inquirer

from platformcommon import PlatformCommon

fullscreen = False
debugging = True
selective_mode = True

class Platform_AtariSTETTFalcon(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'stella', 'hatari']
    # cores = ['hatari_libretro']
    # extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['hatari_libretro']
        
        emulators = ['retroarch', 'stella', 'hatari']
        cores = ['hatari_libretro']
        extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'hatari_libretro':
                extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
                        
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == 'hatari':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarifalcon030', 'atarist', 'atariste', 'ataritt030']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):

        if emulator == 'retroarch':
            if core == 'hatari_libretro':
                extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Atarixlxe(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'other']
    # cores = ['atari800_libretro']
    # extensions = ['st', 'msa', 'zip', 'stx', 'dim', 'ipf', 'm3u', 'xex']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['atari800_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['atari800_libretro']
        extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
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
            if emulator == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):

        if emulator == 'retroarch':
            if core == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_AtariJaguar(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'other']
    # cores = ['virtualjaguar_libretro']
    # extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['virtualjaguar_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['virtualjaguar_libretro']
        extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'virtualjaguar_libretro':
                extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
                
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
            
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
            if emulator == 'virtualjaguar':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijaguar']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'virtualjaguar_libretro':
                extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_AtariLynx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'mednafen']
    # cores = ['handy_libretro', 'mednafen_lynx_libretro']
    # extensions = ['lnx', 'o']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_lynx_libretro']
        
        emulators = ['retroarch', 'mednafen']
        cores = ['handy_libretro', 'mednafen_lynx_libretro']
        extensions = ['lnx', 'o']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'handy_libretro' or core == 'mednafen_lynx_libretro':
                extensions = ['lnx', 'o']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
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
            if emulator == 'mednafen':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarilynx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):

        if emulator == 'retroarch':
            if core == 'handy_libretro' or core == 'mednafen_lynx_libretro':
                extensions = ['lnx', 'o']
        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Atari2600(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'stella']
    # cores = ['stella2014_libretro', 'stella_libretro']
    # extensions = ['zip', 'a26', 'bin']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['stella_libretro']
        
        emulators = ['retroarch', 'stella']
        cores = ['stella2014_libretro', 'stella_libretro']
        extensions = ['zip', 'a26', 'bin']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'stella_libretro':
                extensions = ['zip', 'a26', 'bin']
                
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
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
            if emulator == 'other':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarivcs']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'stella_libretro':
                extensions = ['zip', 'a26', 'bin']
                        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Atari5200(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'atari800']
    # cores = ['atari800_libretro']
    # extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['atari800_libretro']
        
        emulators = ['retroarch', 'atari800']
        cores = ['atari800_libretro']
        extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
                
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
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
            if emulator == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):

        if emulator == 'retroarch':
            if core == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_Atari7800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'prosystem']
    # cores = ['prosystem_libretro']
    # extensions = ['zip', 'a78', 'bin', 'cdf']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['prosystem_libretro']
        
        emulators = ['retroarch', 'prosystem']
        cores = ['prosystem_libretro']
        extensions = ['zip', 'a78', 'bin', 'cdf']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            emulator == emulators[0]
            if selective_mode != False:
                PlatformCommon.multiemu(self,emulators)
            else:
                print('interactive mode is off, using default ' + str(emulators[0]))
                emulator == emulators[0]

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            core == cores[0]
            if selective_mode != False:
                PlatformCommon.multicore(self,cores)
            else:
                print('interactive mode is off, using default ' + str(cores[0]))
                core == cores[0]

        if emulator == 'retroarch':
            if core == 'prosystem_libretro':
                extensions = ['zip', 'a78', 'bin', 'cdf']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core,extensions)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
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
            if emulator == 'other':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atari7800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'prosystem_libretro':
                extensions = ['zip', 'a78', 'bin', 'cdf']
                
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
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files
