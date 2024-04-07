import os
import stat
import os.path

from platformcommon import PlatformCommon

FULLSCREEN = False
DEBUGGING = True


class Platform_Gameboy(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = [
        "gambatte_libretro",
        "mess2016_libretro",
        "mess_libretro",
        "mgba_libretro",
        "tgbdual_libretro",
    ]
    extensions = ["zip", "gb", "dmg", "bin", "u1", "ndd", "zip"]

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ["retroarch"]
        FULLSCREEN = ["False"]
        core = ["mesen-s_libretro"]
        extensions = ["zip", "gb", "dmg", "bin", "u1", "ndd"]

        if emulator[0] == "retroarch":  # gb/c
            if core[0] == "emux_gb_libretro":
                extensions = ["gb", "bin", "rom"]
            if core[0] == "gambatte_libretro":
                extensions = ["gb", "gbc", "dmg"]
            if core[0] == "gearhub_libretro":
                extensions = ["gb", "dmg", "gbc", "cgb", "sgb"]
            if core[0] == "sameboy_libretro":
                extensions = ["gb", "gbc"]
            if core[0] == "tgbdual_libretro":
                extensions = ["cgb", "dmg", "gb", "gbc", "sgb"]
            # gba
            if core[0] == "mgba_libretro":
                extensions = ["gb", "gbc", "gba"]
            if core[0] == "tempgba_libretro":
                extensions = ["gba", "bin", "agb", "gbz"]
            if core[0] == "mednafen_gba_libretro":
                extensions = ["gba", "agb", "bin"]
            # snes
            if (
                    core[0] == "higan_sfc_libretro"
                    or core[0] == "higan_sfc balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bml", "rom"]
            if core[0] == "mesen-s_libretro":
                extensions = ["sfc", "smc", "fig", "swc", "bs", "gb", "gbc"]

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
        return ["gameboy"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            # gb/c
            if core[0] == "emux_gb_libretro":
                extensions = ["gb", "bin", "rom"]
            if core[0] == "gambatte_libretro":
                extensions = ["gb", "gbc", "dmg"]
            if core[0] == "gearhub_libretro":
                extensions = ["gb", "dmg", "gbc", "cgb", "sgb"]
            if core[0] == "sameboy_libretro":
                extensions = ["gb", "gbc"]
            if core[0] == "tgbdual_libretro":
                extensions = ["cgb", "dmg", "gb", "gbc", "sgb"]
            # gba
            if core[0] == "mgba_libretro":
                extensions = ["gb", "gbc", "gba"]
            if core[0] == "tempgba_libretro":
                extensions = ["gba", "bin", "agb", "gbz"]
            if core[0] == "mednafen_gba_libretro":
                extensions = ["gba", "agb", "bin"]
            # snes
            if (
                    core[0] == "higan_sfc_libretro"
                    or core[0] == "higan_sfc balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bml", "rom"]
            if core[0] == "mesen-s_libretro":
                extensions = ["sfc", "smc", "fig", "swc", "bs", "gb", "gbc"]

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
