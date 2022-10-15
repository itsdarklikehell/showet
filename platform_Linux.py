import os
import os.path
from platformcommon import PlatformCommon

class Platform_Linux(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['none']
    cores = ['none']
    fullscreens = ['false']
    extensions = ['elf', 'exe']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['none']
        core = ['none']
        fullscreen = ['false']
        extensions = ['elf', 'exe']
        
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

        # cd to the datadir
        os.chdir(self.datadir)
        
        # check if there are multiple executable files in the datadir
        if len(files) > 1:
            print("Found multiple executables: ", files, " - not sure which one to run!")
            exit(-1)
        else:
            # print status to console.
            print("\tUsing emulator: " + str(emulator[0]))
            print("\tUsing core: " + str(core[0]))
            print("\tUsing fullscreen: " + str(fullscreen[0]))
            print("Running ", files[0])
            # run the executable
            self.run_process([files[0]])

    def supported_platforms(self):
        return ['linux', 'freebsd', 'raspberrypi' ]

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        extensions = ['elf', 'exe']
        
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
