import os
import os.path
import stat
import inquirer

from platformcommon import PlatformCommon

interactive = True
debugging = True

class Platform_Arcade(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'MAME', 'MESS']
    cores = ['mame_libretro', 'mamemess_libretro',]
    extensions = ['zip', 'chd', '7z', 'cmd']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mame_libretro']
        
        emulators = ['retroarch', 'MAME', 'MESS']
        cores = ['mame_libretro', 'mamemess_libretro',]
        extensions = ['zip', 'chd', '7z', 'cmd']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            PlatformCommon.multiemu(self,emulators)

        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            PlatformCommon.multicore(self,cores)

        if emulator == 'retroarch':
            if core == 'mame_libretro' or core == 'mame2015_libretro' or core == 'mame2016_libretro' or core == 'mamearcade_libretro' or core == 'hbmame_libretro':
                extensions = ['zip', 'chd', '7z', 'cmd']
            if core == 'mame2000_libretro' or core == 'mame2010_libretro' or core == 'mame2009_libretro':
                extensions = ['zip', 'chd', '7z']
            if core == 'mame2003_libretro' or core == 'mame2003_plus_libretro' or core == 'mame2003_midway_libretro':
                extensions = ['zip']

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
        if emulator[0] == 'mame':
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
            if emulator[0] == 'mame':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['arcade']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator == 'retroarch':
            if core == 'mame_libretro' or core == 'mame2015_libretro' or core == 'mame2016_libretro' or core == 'mamearcade_libretro' or core == 'hbmame_libretro':
                extensions = ['zip', 'chd', '7z', 'cmd']
            if core == 'mame2000_libretro' or core == 'mame2010_libretro' or core == 'mame2009_libretro':
                extensions = ['zip', 'chd', '7z']
            if core == 'mame2003_libretro' or core == 'mame2003_plus_libretro' or core == 'mame2003_midway_libretro':
                extensions = ['zip']
        
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
