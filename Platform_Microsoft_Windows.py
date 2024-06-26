from platformcommon import PlatformCommon
import os.path
import os
import stat


class Platform_Microsoft_Windows(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["wine", "proton"]
    cores = ["wine"]
    extensions = ["exe"]
    wineprefix = self.showetdir + '/wineprefix'

    def run(self, emulator, core, extensions):
        emulator = self.emulators[0]
        core = self.cores[0]
        extensions = self.extensions

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
            files = self.find_ext_files(emulator, core, extensions)
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running wine, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == self.emulators[0]:
            exefile = files
        if emulator == self.emulators[1]:
            emulator = emulator + ['-flipname', flipfile, files[0]]

        print("\tGuessed executable file: " + files)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed
        os.putenv("WINEPREFIX", self.wineprefix)

        if not os.path.exists(self.wineprefix):
            os.makedirs(self.wineprefix)
            print("Creating wine prefix: " + str(self.wineprefix))
            os.system('WINEARCH="win64" winecfg')

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

        self.run_process([emulator[0], exepath])

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
        return ["windows", "wild"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core, extensions):
        if emulator == self.emulators[0]:
            if core == self.cores[0]:
                extensions = self.extensions

        ext_files = []  # List to store files we find
        for file in self.prod_files:
            size = os.path.getsize(file)  # Get filesize
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                for ext in extensions:  # Iterate over extensions
                    if file.endswith(ext):  # If file ends with extension
                        os.chmod(file, stat.S_IEXEC)  # Set as executable
                        ext_files.append(file)  # Add filepath to list

                    # If file ends with uppercase extension
                    if file.endswith(ext.upper()):
                        os.chmod(file, stat.S_IEXEC)  # Set as executable
                        ext_files.append(file)  # Add filepath to list
        return ext_files  # Return list of found files
