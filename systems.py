import os
import os.path
import stat

from platformcommon import PlatformCommon


class Platform_Nintendo_3DS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "citra"]
    cores = ["citra_libretro", "citra2018_libretro", "citra_canary_libretro",
             "melonds_libretro", "desmume_libretro", "desmume2015_libretro",]
    extensions = ["3ds", "3dsx", "elf", "axf", "cci", "cxi", "app"]

    def run(self):
        emulator = self.emulators[0]
        core = self.cores[0]
        extensions = self.extensions

        if emulator == self.emulators[0]:
            if core == self.cores[0] or core == self.cores[1] or core == self.cores[2] or core == self.cores[3] or core == self.cores[4] or core == self.cores[5]:
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nintendods"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator == self.emulators[0]:
            if core == self.cores[0] or core == self.cores[1] or core == self.cores[2] or core == self.cores[3] or core == self.cores[4] or core == self.cores[5]:
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


class Platform_Nintendo_N64(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "mupen64plus-glide64",
                 "mupen64plus-glide64-lle", "mupen64plus-gliden64"]
    cores = ["mupen64plus_libretro",
             "mupen64plus_next_libretro", "parallel_n46_libretro"]
    extensions = ["n64", "v64", "z64", "bin", "u1", "ndd"]

    def run(self):
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
            # if emulator == self.emulators[1]:
            #     emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nintendo64"]

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


class Platform_Nintendo_DS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "desmume", "melonds"]
    cores = ["melonds_libretro", "desmume_libretro", "desmume2015_libretro"]
    extensions = ["zip", "nds", "dsi"]

    def run(self):
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
            # if emulator == self.emulators[1]:
            #     emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nintendods"]

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


class Platform_Nintendo_Famicom(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "higan", "emux",
                 "fceumm", "nestopia", "quicknes", "mesen"]
    cores = ["quicknes_libretro", "nestopia_libretro", "mess_libretro", "mess2016_libretro",
             "mesen_libretro", "fceumm_libretro", "fceumm_mod_libretro", "fbneo_nes_libretro"]
    extensions = ["zip", "nes", "fds", "unf",
                  "unif", "qd", "nsf", "bin", "rom"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nesfamicom"]

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


class Platform_Nintendo_FamicomDisksystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "higan", "emux",
                 "fceumm", "nestopia", "quicknes", "mesen"]
    cores = ["quicknes_libretro", "nestopia_libretro", "mess_libretro", "mess2016_libretro",
             "mesen_libretro", "fceumm_libretro", "fceumm_mod_libretro", "fbneo_nes_libretro"]
    extensions = ["zip", "nes", "fds", "unf", "unif", "qd", "nsf"]

    def run(self):
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
            # if emulator == self.emulators[1]:
            #     emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nesfamicom"]

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


class Platform_Nintendo_Gameboy(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["gambatte_libretro", "mess2016_libretro",
             "mess_libretro", "mgba_libretro", "tgbdual_libretro"]
    extensions = ["zip", "gb", "dmg", "bin", "u1", "ndd", "zip"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboy"]

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


class Platform_Nintendo_GameboyColor(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["gambatte_libretro", "mgba_libretro", "tgbdual_libretro"]
    extensions = ["zip", "gbc", "dmg", "bin", "u1", "ndd"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboy", "gameboycolor"]

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


class Platform_Nintendo_GameboyAdvance(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["meteor_libretro", "vba_next_libretro",
             "vbam_libretro", "mgba_libretro", "gpsp_libretro"]
    extensions = ["zip", "gb", "gbc", "gba", "dmg", "agb", "bin", "cgb", "sgb"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboyadvance", "gameboycolor", "gameboy"]

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


class Platform_Nintendo_GameCube(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["dolphin_libretro"]
    extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                  "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gamecube"]

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


class Platform_Nintendo_Pokemini(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["pokemini_libretro"]
    extensions = ["zip", "min"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pokemini"]

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


class Platform_Nintendo_SuperFamicom(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["snes9x_libretro"]
    extensions = ["zip", "sfc", "smc", "fig", "swc", "bs"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["snessuperfamicom"]

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


class Platform_Nintendo_Virtualboy(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["mednafen_vb_libretro"]
    extensions = ["zip", "vb", "vboy", "bin"]

    def run(self):
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
            files = self.find_ext_files(emulator, core)
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator == self.emulators[0]:
            emulator.append('-L')
            emulator.append(core[0])

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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["virtualboy"]

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


class Platform_Nintendo_Wii(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["dolphin_libretro"]
    extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                  "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["wii", "wiiu", "nintendowii"]

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


class Platform_Palm_PalmOS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mu_libretro']
    extensions = ['prc', 'pqa', 'img', 'pdb', 'zip']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['palmos']

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


class Platform_Panasonic_3do(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["4do_libretro", "opera_libretro"]
    extensions = ["iso", "bin", "chd", "cue"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["3do", "4do"]

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


class Platform_Phillips_Cdi(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["samecdi_libretro", "cdi2015_libretro"]
    extensions = ["zip", "chd", "iso"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["palmos"]

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


class Platform_Sega_32X(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'picodrive']
    cores = ['picodrive_libretro', 'blastem_libretro']
    extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md',
                  '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['sega32x']

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


class Platform_Sega_Dreamcast(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'flycast', 'redream']
    cores = ['flycast_libretro', 'flycast_gles2_libretro', 'retrodream_libretro']
    extensions = ['chd', 'cdi', 'elf', 'bin', 'cue',
                  'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['dreamcast']

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


class Platform_Sega_GameGear(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    cores = ['gearsystem_libretro',
             'genesis_plus_gx_libretro', 'fbneo_gg_libretro']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagamegear']

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


class Platform_Sega_Mastersystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    cores = ['genesis_plus_gx_libretro', 'fbneo_sms_libretro',
             'gearsystem_libretro', 'picodrive_libretro', 'smsplus_gx_libreto']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
                  'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segamastersystem', 'segagamegear', 'segasg1000', 'segagenesismegadrive', 'segasaturn', 'segastv']

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


class Platform_Sega_Megadrive(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'dgen']
    cores = ['genesis_plus_gx_libretro',
             'fbneo_md_libretro', 'picodrive_libretro']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
                  'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagenesismegadrive']

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


class Platform_Sega_Saturn(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasaturn']

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


class Platform_Sega_Stv(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segastv']

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


class Platform_Sega_Vmu(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'vemulator']
    cores = ['vemulator_libretro']
    extensions = ['zip', 'vms', 'dci', 'bin']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segavmu']

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


class Platform_Sega_SG1000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'gearsystem']
    cores = ['gearsystem_libretro', 'bluemsx_libretro']
    extensions = ['rom', 'ri', 'mx1', 'mx2',
                  'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasg1000']

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


class Platform_Sinclair_Zxspectrum(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch"]
    cores = ["fuse_libretro", "81_libretro"]
    extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk"]

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["zxenhanced", "spectrum", "zxspectrum"]

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


class Platform_Sinclair_Zx81(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "81"]
    cores = ["fuse_libretro", "81_libretro"]
    extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk"]

    def run(self):
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
            files = self.find_ext_files(emulator, core)
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator == self.emulators[0]:
            print("Using:" + str(emulator))
            emulator.append('-L')
            emulator.append(core[0])

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

        self.run_process(emulator)

    def supported_platforms(self):
        return ["zx81"]

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


class Platform_Snk_Neogeo(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['fbneo_libretro', 'neocd_libretro', 'fbalpha2012_libretro']
    extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeo']

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


class Platform_Snk_NeogeoPocket(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mednafen_ngp_libretro', 'fbneo_ngp']
    extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeopocket']

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


class Platform_Snk_NeogeoPocketColor(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mednafen_ngp_libretro', 'fbneo_ngpc']
    extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeopocketcolor']

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


class Platform_Sony_Ps2(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['pcsx2_libretro', 'play_libretro']
    extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img',
                  'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstation2']

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


class Platform_Sony_Psp(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'ppsspp']
    cores = ['ppsspp_libretro']
    extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstationportable']

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


class Platform_Sony_Psx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['pcsx_rearmed_libretro',
             'mednafen_psx_libretro', 'swanstation_libretro']
    extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img',
                  'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstation']

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


class Platform_SpectraVision_SpectraVideo(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['bluemsx_libretro']
    extensions = ['rom', 'ri', 'mx1', 'mx2',
                  'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['spectravision']

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


class Platform_Thomson_MOTO(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['theodore_libretro']
    extensions = ['fd', 'sap', 'k7', 'm7', 'm5', 'rom']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['thomson']

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


class Platform_Wild_Gamemusic(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['gme_libretro']
    extensions = ['zip', 'ay', 'gbs', 'gym', 'hes',
                  'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']

    def run(self):
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
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'music']

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


class Platform_Wild_VideoFFMPEG(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['ffmpeg_libretro']
    extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                  '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
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
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

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


class Platform_Wild_VideoMPV(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mpv_libretro']
    extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                  '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
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

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

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
