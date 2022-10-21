import os
import os.path
import stat

from platformcommon import PlatformCommon

fullscreen = False
debugging = True
selective_mode = False

class Platform_Xbox(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['directxbox_libretro']
    extensions = ['zip', 'iso']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['directxbox_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['directxbox_libretro']
        extensions = ['zip', 'iso']

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

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'other':
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

class Platform_Msx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'openmsx', 'openmsx-msx2', 'openmsx-msx2-plus', 'openmsx-msx-turbo']
    cores = ['bluemsx_libretro', 'fbneo_msx_libretro', 'fmsx_libretro']
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
        extensions = ['rom', 'ri', 'mx1', 'mx2', 'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'other':
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
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['msx', 'msx2', 'msx2plus', 'msxturbor', 'spectravideo3x8']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator[0] == 'other':
            extensions = ['unknown']
            
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

class Platform_Windows(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['wine', 'other']
    cores = ['wine']
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
        extensions = ['exe']
        wineprefix = self.showetdir + '/wineprefix'
        
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
        if emulator[0] == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')
        
        if emulator == 'wine':
            exefile = files[0]

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

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

        if emulator == 'wine':
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