import os
import os.path
from platformcommon import PlatformCommon

class Platform_Msdos(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'dosbox']
    cores = ['dosbox_core_libretro', 'dosbox_pure_libretro', 'dosbox_svn_libretro', 'dosbox_svn_ce_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8', 'conf']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['dosbox_core_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'exe', 'com', 'bat', 'conf']
        
        if emulator == 'retroarch':
            if core == 'dosbox_core_libretro' or core == 'dosbox_svn_libretro' or core == 'dosbox_svn_ce_libretro':
                extensions = ['exe', 'com', 'bat', 'conf', 'cue', 'iso']
            if core == 'dosbox_pure_libretro':
                extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8', 'conf']
        
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary    
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:          
        if emulator[0] == 'dosbox':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

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
            if emulator[0] == 'dosbox':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['msdos', 'msdosgus', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        if emulator[0] == 'retroarch':
            if core[0] == 'dosbox_core_libretro' or core[0] == 'dosbox_svn_libretro' or core[0] == 'dosbox_svn_ce_libretro':
                extensions = ['exe', 'com', 'bat', 'conf', 'cue', 'iso']
            if core[0] == 'dosbox_pure_libretro':
                extensions = ['zip', 'dosz', 'exe', 'com', 'bat', 'iso', 'cue', 'ins', 'img', 'ima', 'vhd', 'jrc', 'tc', 'm3u', 'm3u8', 'conf']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
        
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    
                    if file.endswith(ext):
                        if file == 'dos4gw.exe' or file == 'DOS4GW.EXE':
                            print("\tFound dos4gw.exe file: skipping for now... ")
                            #ext_files.append(file)
                        else:
                            ext_files.append(file)
                            print("\tFound file: " + file)
                    
                    if file.endswith(ext.upper()):
                        if file == 'dos4gw.exe' or file == 'DOS4GW.EXE':
                            print("\tFound dos4gw.exe file: skipping for now... ")
                            #ext_files.append(file)
                        else:
                            ext_files.append(file)
                            print("\tFound file: " + file)
        
        return ext_files
