import os
import stat
import os.path

from platformcommon import PlatformCommon

FULLSCREEN = False
DEBUGGING = True


class Platform_FamicomDisksystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "higan", "emux",
    #              "fceumm", "nestopia", "quicknes", "mesen"]
    # cores = ["quicknes_libretro", "nestopia_libretro", "mess_libretro", "mess2016_libretro",
    #          "mesen_libretro", "fceumm_libretro", "fceumm_mod_libretro", "fbneo_nes_libretro"]
    # extensions = ["zip", "nes", "fds", "unf", "unif", "qd", "nsf"]

    def run(self):
        emulator = ["retroarch"]
        core = ["quicknes_libretro"]
        extensions = ["zip", "nes", "fds", "unf", "unif", "qd", "nsf"]

        if emulator[0] == "retroarch":
            if core[0] == "quicknes_libretro" or core[0] == "bnes_libretro":
                extensions = ["nes"]
            if core[0] == "emux_nes_libretro":
                extensions = ["nes", "bin", "rom"]
            if (
                    core[0] == "nestopia_libretro"
                    or core[0] == "fceumm_libretro"
                    or core[0] == "mesen_libretro"
            ):
                extensions = ["fds", "nes", "unif", "unf"]

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
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "other":
            # Set whether we should run in fullscreens or not.
            if FULLSCREEN is True:
                emulator.append("--fullscreen")

        # print status to console.
        if DEBUGGING is not False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nesfamicom"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == "quicknes_libretro" or core[0] == "bnes_libretro":
                extensions = ["nes"]
            if core[0] == "emux_nes_libretro":
                extensions = ["nes", "bin", "rom"]
            if (
                    core[0] == "nestopia_libretro"
                    or core[0] == "fceumm_libretro"
                    or core[0] == "mesen_libretro"
            ):
                extensions = ["fds", "nes", "unif", "unf"]

        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if DEBUGGING is not False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if DEBUGGING is not False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files
