import os
import os.path
import stat
import inquirer

from platformcommon import PlatformCommon

fullscreen = False
debugging = True
selective_mode = False

class Platform_Msdos(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'dosbox']
    # cores = ['dosbox_core_libretro', 'dosbox_pure_libretro', 'dosbox_svn_libretro', 'dosbox_svn_ce_libretro']
    # extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['dosbox_core_libretro']
        
        emulators = ['retroarch', 'dosbox']
        cores = ['dosbox_core_libretro', 'dosbox_pure_libretro', 'dosbox_svn_libretro', 'dosbox_svn_ce_libretro']
        extensions = ['zip', 'exe', 'com', 'bat', 'conf']


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
                
        if emulator == 'other':
            extensions = ['unknown']
        if emulator == 'retroarch':
            if core == 'dosbox_core_libretro' or core == 'dosbox_svn_libretro' or core == 'dosbox_svn_ce_libretro':
                extensions = ['exe', 'com', 'bat', 'conf', 'cue', 'iso']
            if core == 'dosbox_pure_libretro':
                extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8']
        
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
            if emulator == 'dosbox':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['msdos', 'msdosgus', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core,extensions):
        if emulator == 'other':
            extensions = ['unknown']
            
        if emulator == 'retroarch':
            if core == 'dosbox_core_libretro' or core == 'dosbox_svn_libretro' or core == 'dosbox_svn_ce_libretro':
                extensions = ['exe', 'com', 'bat', 'conf', 'cue', 'iso']
            if core == 'dosbox_pure_libretro':
                extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8']
        
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
