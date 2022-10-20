import os
import os.path
import stat
import inquirer

from platformcommon import PlatformCommon

interactive = True
debugging = True

class Platform_Linux(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['linux']
    cores = ['linux']
    extensions = ['elf', 'exe']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['bash']
        core = ['bash']
        
        emulators = ['linux']
        cores = ['linux']
        extensions = ['elf', 'exe']

        # If multiple emulators are specified (e.g. 'retroarch', 'dosbox') ask the user to specify which one to use.
        if len(emulators) > 1:
            PlatformCommon.multiemu(self,emulators)
        else:
            emulator = emulators[0]
        
        # If multiple cores are specified (e.g. 'dosbox_libretro', 'dosbox_pure_libretro') ask the user to specify which one to use.
        if len(cores) > 1:
            PlatformCommon.multicore(self,cores)
        else:
            core = core[0]   
     
        if emulator[0] == 'bash':
            if core[0] == 'bash':
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
