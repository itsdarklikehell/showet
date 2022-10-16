import os
import os.path
from platformcommon import PlatformCommon

class Platform_Linux(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['linux']
    cores = ['linux']
    fullscreens = ['false']
    streamings = ['twitch', 'youtube', 'restream']
    recordings = ['true']
    extensions = ['elf', 'exe']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['bash']
        core = ['bash']
        fullscreen = ['false']
        streaming = ['restream']
        recording = ['true']
        extensions = ['elf', 'exe']
        
        if emulator == 'bash':
            if core == 'bash':
                extensions = ['elf', 'exe']
                
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

        # cd to the datadir
        os.chdir(self.datadir)
        
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
            
        # check if there are multiple executable files in the datadir
        if len(files) > 1:
            print("Found multiple executables: ", files, " - not sure which one to run!")
            exit(-1)
        else:
            print("Running ", files[0])
            emulator = emulator + [files[0]]
            self.run_process(emulator)

    def supported_platforms(self):
        return ['linux', 'freebsd', 'raspberrypi' ]

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):
        extensions = ['elf', 'exe']
        
        if emulator[0] == 'bash':
            if core[0] == 'bash':
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
