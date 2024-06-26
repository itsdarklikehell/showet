from platformcommon import PlatformCommon
import os
import stat


class Platform_Linux_Linux(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["bash"]
    cores = ["bash"]
    extensions = ["elf", "exe"]

    def run(self):
        emulator = self.emulators[0]
        core = self.cores[0]
        extensions = self.extensions
        emulator = "bash"
        core = "bash"

        if emulator == self.emulators[0]:
            if core == self.cores[0]:
                extensions = self.extensions

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator, core)
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == self.emulators[0]:
            emulator.append('-L')
            emulator.append(core[0])

        # cd to the datadir
        os.chdir(self.datadir)

        # drives = []
        # # Support only one for now..
        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            
            with open(flipfile, "w") as f:
                # f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                # f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")

            if emulator == self.emulators[0]:
                emulator = emulator + [files[0]]
            if emulator == self.emulators[1]:
                emulator = emulator + ['-flipname', flipfile, files[0]]

        # check if there are multiple executable files in the datadir
        if len(files) > 1:
            print(
                "Found multiple executables: ", files, " - not sure which one to run!"
            )
            exit(-1)
        else:
            print("Running ", files[0])
            emulator = emulator + [files[0]]

            self.run_process(emulator)

    # Returns the list of supported platforms for this platform.
    #
    # Returns:
    #     List of supported platforms.
    def supported_platforms(self):
        """
        Returns the list of supported platforms for this platform.

        Returns:
            List of supported platforms.
        """
        return ["linux", "freebsd", "raspberrypi"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator == self.emulators[0]:
            if core == self.cores[0]:
                extensions = self.extensions

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files