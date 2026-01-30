from platformcommon import PlatformCommon
import os
import stat

class Platform_Enterprise_Ep128(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "ep128"]
    cores = ["ep128emu_libretro"]
    extensions = ["zip", "img", "dsk", "tap", "dtf", "com",
                  "trn", "128", "bas", "cas", "cdt", "tzx", "."]

    def run(self):
        """
        Runs the platform.
        """
        # Set up the emulator and core to run.
        emulator = self.emulators[0]
        core = self.cores[0]
        extensions = self.extensions

        # If we are running RetroArch, we need to provide the libretro core.
        if emulator == self.emulators[0]:
            if core == self.cores[0]:
                extensions = self.extensions

        # Look for files with the given extensions.
        # If not found, try to identify files by UPPERCASE extensions.
        # If not found, try to identify files by any magic necessary.
        ext_ = []
        for ext_ in extensions:
            files = self.find_files_with_extension(ext_)
            if len(files) == 0:
                files = self.find_files_with_extension(ext_.upper())
            if len(files) == 0:
                files = self.find_ext_files(emulator, core)
            # if len(files) == 0:
            #     files = self.find_magic_cookies()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # In case we are running RetroArch, we need to provide some arguments to set the libretro core.
        if emulator == self.emulators[0]:
            emulator.append('-L')
            emulator.append(core[0])

        # Support only one disk for now..
        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)

            # Create a fliplist for RetroArch.
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

            # Set up arguments for running the emulator.
            if emulator == self.emulators[0]:
                emulator = emulator + [files[0]]
            if emulator == self.emulators[1]:
                emulator = emulator + ['-flipname', flipfile, files[0]]

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
        return ["enterprise"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        """
        Finds all files with supported extensions and sets them as executable.

        Returns:
            List with filepaths to all found files.
        """
        if emulator == self.emulators[0]:
            if core == self.cores[0]:
                extensions = self.extensions  # List of extensions to look for

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
