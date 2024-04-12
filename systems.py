import os
import stat
import os.path

from platformcommon import PlatformCommon


class Platform_Amstrad_Cpcplus(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "zesarux"]
    # cores = ["crocods_libretro", "cap32_libretro"]
    # extensions = ["dsk", "sna", "zip", "tap", "cdt", "voc", "cpr", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["cap32_libretro"]
        extensions = ["dsk", "sna", "zip", "tap", "cdt", "voc", "cpr", "m3u"]

        if emulator[0] == "retroarch":
            if core[0] == "crocods_libretro":
                extensions = ["dsk", "sna", "kcr"]
            if core[0] == "cap32_libretro":
                extensions = ["dsk", "sna", "zip",
                              "tap", "cdt", "voc", "cpr", "m3u"]

        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "zesarux":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "zesarux":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["amstradplus", "amstradcpc"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "crocods_libretro":
                extensions = ["dsk", "sna", "kcr"]
            if core[0] == "cap32_libretro":
                extensions = ["dsk", "sna", "zip",
                              "tap", "cdt", "voc", "cpr", "m3u"]

        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Apple_AppleI(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "linapple", "basilisk"]
    # cores = ["minivmac_libretro"]
    # extensions = ["dsk", "img", "zip", "hvf", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["minivmac_libretro"]
        extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "linapple":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "linapple":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["appleii", "appleiigs"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Apple_AppleII(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "linapple", "basilisk"]
    # cores = ["minivmac_libretro"]
    # extensions = ["dsk", "img", "zip", "hvf", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["minivmac_libretro"]
        extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "linapple":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "linapple":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["appleii", "appleiigs"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Apple_AppleIIGS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "linapple", "basilisk"]
    # cores = ["minivmac_libretro"]
    # extensions = ["dsk", "img", "zip", "hvf", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["minivmac_libretro"]
        extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "linapple":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "linapple":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["appleii", "appleiigs"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "minivmac_libretro":
                extensions = ["dsk", "img", "zip", "hvf", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Arcade_Arcade(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "MAME", "MESS"]
    # cores = ["mame_libretro", "mamemess_libretro"]
    # extensions = ["zip", "chd", "7z", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mame_libretro"]
        extensions = ["zip", "chd", "7z", "cmd"]
        if emulator[0] == "retroarch":
            if (
                    core[0] == "mame_libretro"
                    or core[0] == "mame2015_libretro"
                    or core[0] == "mame2016_libretro"
                    or core[0] == "mamearcade_libretro"
                    or core[0] == "hbmame_libretro"
            ):
                extensions = ["zip", "chd", "7z", "cmd"]
            if (
                    core[0] == "mame2000_libretro"
                    or core[0] == "mame2010_libretro"
                    or core[0] == "mame2009_libretro"
            ):
                extensions = ["zip", "chd", "7z"]
            if (
                    core[0] == "mame2003_libretro"
                    or core[0] == "mame2003_plus_libretro"
                    or core[0] == "mame2003_midway_libretro"
            ):
                extensions = ["zip"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "mame":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "mame":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["arcade"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if (
                    core[0] == "mame_libretro"
                    or core[0] == "mame2015_libretro"
                    or core[0] == "mame2016_libretro"
                    or core[0] == "mamearcade_libretro"
                    or core[0] == "hbmame_libretro"
            ):
                extensions = ["zip", "chd", "7z", "cmd"]
            if (
                    core[0] == "mame2000_libretro"
                    or core[0] == "mame2010_libretro"
                    or core[0] == "mame2009_libretro"
            ):
                extensions = ["zip", "chd", "7z"]
            if (
                    core[0] == "mame2003_libretro"
                    or core[0] == "mame2003_plus_libretro"
                    or core[0] == "mame2003_midway_libretro"
            ):
                extensions = ["zip"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Archimedes_Acorn(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["mame_libretro", "mame2016_libretro"]
    # extensions = ["zip", "chd", "7z", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mame_libretro"]
        extensions = ["zip", "chd", "7z", "cmd"]
        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "mame":
            print("Using: " + str(emulator))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "mame":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["acorn"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Atari_2600(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'stella']
    # cores = ['stella2014_libretro', 'stella_libretro']
    # extensions = ['zip', 'a26', 'bin']

    def run(self):
        emulator = ["retroarch"]
        core = ['stella_libretro']
        extensions = ['zip', 'a26', 'bin']
        if emulator[0] == "retroarch":
            if core[0] == 'stella_libretro':
                extensions = ['zip', 'a26', 'bin']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarivcs']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'stella_libretro':
                extensions = ['zip', 'a26', 'bin']
        if emulator[0] == "other":
            extensions = ['unknown']

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


class Platform_Atari_5200(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'atari800']
    # cores = ['atari800_libretro']
    # extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas',
    #               'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']

    def run(self):
        emulator = ["retroarch"]
        core = ['atari800_libretro']
        extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas',
                      'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "retroarch":
            if core[0] == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin',
                              'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin',
                              'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Atari_7800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'prosystem']
    # cores = ['prosystem_libretro']
    # extensions = ['zip', 'a78', 'bin', 'cdf']

    def run(self):
        emulator = ["retroarch"]
        core = ['prosystem_libretro']
        extensions = ['zip', 'a78', 'bin', 'cdf']
        if emulator[0] == "retroarch":
            if core[0] == 'prosystem_libretro':
                extensions = ['zip', 'a78', 'bin', 'cdf']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atari7800']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'prosystem_libretro':
                extensions = ['zip', 'a78', 'bin', 'cdf']
        if emulator[0] == "other":
            extensions = ['unknown']

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


class Platform_Atari_Jaguar(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'other']
    # cores = ['virtualjaguar_libretro']
    # extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']

    def run(self):
        emulator = ["retroarch"]
        core = ['virtualjaguar_libretro']
        extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
        if emulator[0] == "retroarch":
            if core[0] == 'virtualjaguar_libretro':
                extensions = ['zip', 'j64', 'jag',
                              'rom', 'abs', 'cof', 'bin', 'prg']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'virtualjaguar':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijaguar']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'virtualjaguar_libretro':
                extensions = ['zip', 'j64', 'jag',
                              'rom', 'abs', 'cof', 'bin', 'prg']
        if emulator[0] == "other":
            extensions = ['unknown']

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


class Platform_Atari_Lynx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'mednafen']
    # cores = ['handy_libretro', 'mednafen_lynx_libretro']
    # extensions = ['lnx', 'o']

    def run(self):
        emulator = ["retroarch"]
        core = ['mednafen_lynx_libretro']
        extensions = ['lnx', 'o']
        if emulator[0] == "retroarch":
            if core[0] == 'handy_libretro' or core[0] == 'mednafen_lynx_libretro':
                extensions = ['lnx', 'o']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'mednafen':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarilynx']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'handy_libretro' or core[0] == 'mednafen_lynx_libretro':
                extensions = ['lnx', 'o']
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Atari_STETTFalcon(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'stella', 'hatari']
    # cores = ['hatari_libretro', 'a5200_libretro']
    # extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['hatari_libretro', 'a5200_libretro']
        extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'hatari_libretro':
                extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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

            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'hatari':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarifalcon030', 'atarist', 'atariste', 'ataritt030']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == 'hatari_libretro':
                extensions = ['st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Atari_xlxe(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'other']
    # cores = ['atari800_libretro']
    # extensions = ['st', 'msa', 'zip', 'stx', 'dim', 'ipf', 'm3u', 'xex']

    def run(self):
        emulator = ["retroarch"]
        core = ['atari800_libretro']
        extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin',
                      'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "retroarch":
            if core[0] == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin',
                              'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'atari800_libretro':
                extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin',
                              'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Bandai_Wonderswan(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "mednafen"]
    # cores = ["mednafen_wswan_libretro"]
    # extensions = ["zip", "ws", "wsc", "pc2"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mednafen_wswan_libretro"]
        extensions = ["zip", "ws", "wsc", "pc2"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_wswan_libretro":
                extensions = ["ws", "wsc", "pc2"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "mednafen":
                emulator = emulator + ["-flipname", flipfile, files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["wonderswan", "wonderswancolor"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_wswan_libretro":
                extensions = ["ws", "wsc", "pc2"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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


class Platform_Coleco_Colecovision(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "bluemsx", "gearcoleco"]
    # cores = ["bluemsx_libretro", "gearcoleco_libretro"]
    # extensions = ["rom", "ri", "mx1", "mx2", "col", "dsk", "cas", "sg", "sc", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["bluemsx_libretro"]
        extensions = ["rom", "ri", "mx1", "mx2",
                      "col", "dsk", "cas", "sg", "sc", "m3u"]
        if emulator[0] == "retroarch":
            if core[0] == "bluemsx_libretro":
                extensions = ["rom", "ri", "mx1", "mx2",
                              "col", "dsk", "cas", "sg", "sc", "m3u"]
            if core[0] == "gearcoleco_libretro":
                extensions = ["col", "cv", "bin", "rom"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["Coleco", "Colecovision"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "bluemsx_libretro":
                extensions = ["rom", "ri", "mx1", "mx2",
                              "col", "dsk", "cas", "sg", "sc", "m3u"]
            if core[0] == "gearcoleco_libretro":
                extensions = ["col", "cv", "bin", "rom"]

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


class Platform_Commodore_64(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch"]
    # cores = ['vice_x64sc_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82',
    #                'd8z', 'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_x64sc_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82',
                       'd8z', 'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vice_x64sc_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
            tapes_ext = ['t64', 'tap', 'tcrt']
            roms_ext = ['prg', 'p00', 'crt', 'bin']
            vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
            extensions = []
            extensions.extend(floppys_ext)
            extensions.extend(tapes_ext)
            extensions.extend(roms_ext)
            extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore64']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_x64sc_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
            tapes_ext = ['t64', 'tap', 'tcrt']
            roms_ext = ['prg', 'p00', 'crt', 'bin']
            vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
            extensions = []
            extensions.extend(floppys_ext)
            extensions.extend(tapes_ext)
            extensions.extend(roms_ext)
            extensions.extend(vic20_ext)

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


class Platform_Commodore_128(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'vice']
    # cores = ['vice_x128_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
    #                'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_x128_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                       'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "retroarch":
            if core[0] == 'vice_x128_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore128']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_x128_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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


class Platform_Commodore_Amiga(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'puae', 'fs-uae']
    # cores = ['puae2021_libretro', 'puae_libretro',
    #          'fsuae_libretro', 'uae4arm_libretro']
    # floppys_ext = ['adf', 'adz', 'dms', 'fdi', 'ipf']
    # harddrives_ext = ['hdf', 'hdz', 'datadir']
    # whdload_ext = ['lha', 'slave', 'info']
    # cd_ext = ['cue', 'ccd', 'nrg', 'mds', 'iso']
    # other = ['uae', 'm3u', 'zip', '7z']
    # extensions = []
    # extensions.append(other)
    # extensions.append(floppys_ext)
    # extensions.append(harddrives_ext)
    # extensions.append(whdload_ext)
    # extensions.append(cd_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['puae_libretro']
        floppys_ext = ['adf', 'adz', 'dms', 'fdi', 'ipf']
        harddrives_ext = ['hdf', 'hdz', 'datadir']
        whdload_ext = ['lha', 'slave', 'info']
        cd_ext = ['cue', 'ccd', 'nrg', 'mds', 'iso']
        other = ['uae', 'm3u', 'zip', '7z']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(harddrives_ext)
        extensions.extend(whdload_ext)
        extensions.extend(cd_ext)
        extensions.extend(other)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'puae_libretro':
                floppys_ext = ['adf', 'adz', 'dms', 'fdi', 'ipf']
                harddrives_ext = ['hdf', 'hdz', 'datadir']
                whdload_ext = ['lha', 'slave', 'info']
                cd_ext = ['cue', 'ccd', 'nrg', 'mds', 'iso']
                other = ['uae', 'm3u', 'zip', '7z', 'rp9']
                extensions = []
                extensions.extend(other)
                extensions.extend(floppys_ext)
                extensions.extend(harddrives_ext)
                extensions.extend(whdload_ext)
                extensions.extend(cd_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
            # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['amigaocsecs', 'amigaaga', 'amigappcrtg']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'puae_libretro':
                floppys_ext = ['adf', 'adz', 'dms', 'fdi', 'ipf']
                harddrives_ext = ['hdf', 'hdz', 'datadir']
                whdload_ext = ['lha', 'slave', 'info']
                cd_ext = ['cue', 'ccd', 'nrg', 'mds', 'iso']
                other = ['uae', 'm3u', 'zip', '7z']
                extensions = []
                extensions.extend(other)
                extensions.extend(floppys_ext)
                extensions.extend(harddrives_ext)
                extensions.extend(whdload_ext)
                extensions.extend(cd_ext)

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


class Platform_Commodore_CBMII(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'vice']
    # cores = ['vice_xcbm2_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
    #                'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_xcbm2_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                       'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xcbm2_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodorecbm']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xcbm2_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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


class Platform_Commodore_Pet(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'vice']
    # cores = ['vice_xpet_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
    #                'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_xpet_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                       'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xpet_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodorepet']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xpet_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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


class Platform_Commodore_Plus4(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'vice']
    # cores = ['vice_xplus4_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
    #                'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_xplus4_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                       'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xplus4_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodoreplus4', 'c16116plus4']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xplus4_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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


class Platform_Commodore_Vic20(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'vice']
    # cores = ['vice_xvic_libretro']
    # floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
    #                'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
    # tapes_ext = ['t64', 'tap', 'tcrt']
    # roms_ext = ['prg', 'p00', 'crt', 'bin']
    # vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
    # extensions = []
    # extensions.extend(floppys_ext)
    # extensions.extend(tapes_ext)
    # extensions.extend(roms_ext)
    # extensions.extend(vic20_ext)

    def run(self):
        emulator = ["retroarch"]
        core = ['vice_xvic_libretro']
        floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                       'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
        tapes_ext = ['t64', 'tap', 'tcrt']
        roms_ext = ['prg', 'p00', 'crt', 'bin']
        vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
        extensions = []
        extensions.extend(floppys_ext)
        extensions.extend(tapes_ext)
        extensions.extend(roms_ext)
        extensions.extend(vic20_ext)
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xvic_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['vic20']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'vice_xvic_libretro':
                floppys_ext = ['d64', 'd6z', 'd71', 'd7z', 'd80', 'd8z', 'd81', 'd82', 'd8z',
                               'g64', 'g6z', 'g41', 'g4z', 'x64', 'x6z', 'nib', 'nbz', 'd2m', 'd4m']
                tapes_ext = ['t64', 'tap', 'tcrt']
                roms_ext = ['prg', 'p00', 'crt', 'bin']
                vic20_ext = ['20', '40', '60', 'a0', 'b0', 'rom']
                extensions = []
                extensions.extend(floppys_ext)
                extensions.extend(tapes_ext)
                extensions.extend(roms_ext)
                extensions.extend(vic20_ext)

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


class Platform_Elektronika_Pdp11(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "m"]
    # cores = ["bk_libretro"]
    # extensions = ["bin"]

    def run(self):
        emulator = ["retroarch"]
        core = ["bk_libretro"]
        extensions = ["bin"]
        if emulator[0] == "retroarch":
            if core[0] == "bk_libretro":
                extensions = ["bin"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "bk":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["bk001010", "bk001011m"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "bk_libretro":
                extensions = ["bin"]

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


class Platform_Enterprise_Ep128(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["ep128emu_libretro"]
    # extensions = ["zip", "img", "dsk", "tap", "dtf", "com",
    #               "trn", "128", "bas", "cas", "cdt", "tzx", "."]

    def run(self):
        emulator = ["retroarch"]
        core = ["ep128emu_libretro"]
        extensions = ["zip", "img", "dsk", "tap", "dtf", "com",
                      "trn", "128", "bas", "cas", "cdt", "tzx", "."]
        if emulator[0] == "retroarch":
            if core[0] == "ep128emu_libretro":
                extensions = ["img", "dsk", "tap", "dtf", "com", "trn",
                              "128", "bas", "cas", "cdt", "tzx", "tvcwav", ".",]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["enterprise"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == "ep128emu_libretro":
                extensions = ["img", "dsk", "tap", "dtf", "com", "trn",
                              "128", "bas", "cas", "cdt", "tzx", "tvcwav", "."]

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


class Platform_Fairchild_Channelf(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "freechaf"]
    # cores = ["freechaf_libretro"]
    # extensions = ["zip", "bin", "chf"]

    def run(self):
        emulator = ["retroarch"]
        core = ["freechaf_libretro"]
        extensions = ["zip", "bin", "chf"]
        if emulator[0] == "retroarch":
            if core[0] == "freechaf_libretro":
                extensions = ["bin", "chf"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "freechaf":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["fairchild", "channelf"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "freechaf_libretro":
                extensions = ["bin", "chf"]

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


class Platform_FanCon_Pico8(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["retro8_libretro"]
    # extensions = ["zip", "p8", "png"]

    def run(self):
        emulator = ["retroarch"]
        core = ["retro8_libretro"]
        extensions = ["zip", "p8", "png"]
        if emulator[0] == "retroarch":
            if core[0] == "retro8_libretro":
                extensions = ["p8", "png"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pico8"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "retro8_libretro":
                extensions = ["p8", "png"]

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


class Platform_FanCon_Tic80(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ['retroarch', 'other']
    # cores = ['tic80_libretro']
    # extensions = ['zip', 'tic']

    def run(self):
        emulator = ["retroarch"]
        core = ['tic80_libretro']
        extensions = ['zip', 'tic']
        if emulator[0] == "retroarch":
            if core[0] == 'tic80_libretro':
                extensions = ['tic']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['tic80']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'tic80_libretro':
                extensions = ['tic']

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


class Platform_Gamepark_32(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["mame_libretro"]
    # extensions = ["zip", "chd", "7z", "cmd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mame_libretro"]
        extensions = ["zip", "chd", "7z", "cmd"]
        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameparkgp32"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]

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


class Platform_Gamepark_2X(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ["retroarch", "other"]
    cores = ["mame_libretro"]
    extensions = ["zip", "chd", "7z", "cmd"]

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ["retroarch"]
        core = ["mame_libretro"]
        extensions = ["zip", "chd", "7z", "cmd"]

        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]

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
        return ["gameparkgp2x"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == "mame_libretro":
                extensions = ["zip", "chd", "7z", "cmd"]

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


class Platform_GCE_Vectrex(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "vecx"]
    # cores = ["vecx_libretro"]
    # extensions = ["zip", "bin", "vec"]

    def run(self):
        emulator = ["retroarch"]
        core = ["vecx_libretro"]
        extensions = ["zip", "bin", "vec"]
        if emulator[0] == "retroarch":
            if core[0] == "vecx_libretro":
                extensions = ["bin", "vec"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "vecx":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["vectrex"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "vecx_libretro":
                extensions = ["bin", "vec"]

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


class Platform_Java_Java(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["squirreljme_libretro"]
    # extensions = ["zip", "jar", "sqc", "jam", "jad", "kjx"]

    def run(self):
        emulator = ["retroarch"]
        core = ["squirreljme_libretro"]
        extensions = ["zip", "jar", "sqc", "jam", "jad", "kjx"]
        if emulator[0] == "retroarch":
            if core[0] == "squirreljme_libretro":
                extensions = ["jar", "sqc", "jam", "jad", "kjx"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["java", "javascript"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "squirreljme_libretro":
                extensions = ["jar", "sqc", "jam", "jad", "kjx"]

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


class Platform_Linux_Linux(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["linux"]
    # cores = ["linux"]
    # extensions = ["elf", "exe"]

    def run(self):
        emulator = ["bash"]
        core = ["bash"]
        extensions = ["elf", "exe"]
        if emulator[0] == "bash":
            if core[0] == "bash":
                extensions = ["elf", "exe"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])

        # cd to the datadir
        os.chdir(self.datadir)

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

    def supported_platforms(self):
        return ["linux", "freebsd", "raspberrypi"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        extensions = ["elf", "exe"]
        if emulator[0] == "bash":
            if core[0] == "bash":
                extensions = ["elf", "exe"]

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


class Platform_Magnavox_Odyssey(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["o2em_libretro"]
    # extensions = ["zip", "bin"]

    def run(self):
        emulator = ["retroarch"]
        core = ["o2em_libretro"]
        extensions = ["zip", "bin"]
        if emulator[0] == "retroarch":
            if core[0] == "o2em_libretro":
                extensions = ["bin"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "o2em":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["intellivision"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "o2em_libretro":
                extensions = ["bin"]

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


class Platform_Mattel_Intellivision(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["freeintv_libretro", "jzintv", "jzintv-ecs"]
    # extensions = ["int", "bin", "rom"]

    def run(self):
        emulator = ["retroarch"]
        core = ["freeintv_libretro"]
        extensions = ["int", "bin", "rom"]
        if emulator[0] == "retroarch":
            if core[0] == "freeintv_libretro":
                extensions = ["int", "bin", "rom"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "freeintv":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["intellivision"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "freeintv_libretro":
                extensions = ["int", "bin", "rom"]

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


class Platform_Microsoft_Msx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "openmsx", "openmsx-msx2", "openmsx-msx2-plus", "openmsx-msx-turbo",]    cores = ["bluemsx_libretro", "fbneo_msx_libretro", "fmsx_libretro"]
    # extensions = ["rom", "ri", "mx1", "mx2",
    #               "col", "dsk", "cas", "sg", "sc", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["bluemsx_libretro"]
        extensions = ["rom", "ri", "mx1", "mx2",
                      "col", "dsk", "cas", "sg", "sc", "m3u"]
        if emulator[0] == "retroarch":
            if core[0] == "bluemsx_libretro":
                extensions = ["rom", "ri", "mx1", "mx2",
                              "col", "dsk", "cas", "sg", "sc", "m3u",]
            if core[0] == "fmsx_libretro":
                extensions = ["rom", "mx1", "mx2", "dsk", "fdi", "cas", "m3u"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["msx", "msx2", "msx2plus", "msxturbor", "spectravideo3x8"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "bluemsx_libretro":
                extensions = ["rom", "ri", "mx1", "mx2",
                              "col", "dsk", "cas", "sg", "sc", "m3u"]
            if core[0] == "fmsx_libretro":
                extensions = ["rom", "mx1", "mx2", "dsk", "fdi", "cas", "m3u"]

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


class Platform_Microsoft_Windows(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["wine", "other"]
    # cores = ["wine"]
    # extensions = ["exe"]
    # wineprefix = self.showetdir + '/wineprefix'

    def run(self):
        emulator = ["wine"]
        core = ["wine"]
        extensions = ["exe"]
        wineprefix = self.showetdir + "/wineprefix"

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "other":
            # Set whether we should run in fullscreens or not.
            if FULLSCREEN is True:
                emulator.append("--fullscreen")
        if emulator[0] == "wine":
            exefile = files

        # print status to console.
        if DEBUGGING is not False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tSearching for extensions: " + str(extensions))

            print("\tGuessed executable file: " + exefile)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed
        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process([emulator[0], exepath])

    def supported_platforms(self):
        return ["windows", "wild"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "wine":
            if core[0] == "wine":
                extensions = ["exe"]

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


class Platform_Microsoft_Xbox(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["directxbox_libretro"]
    # extensions = ["zip", "iso"]

    def run(self):
        emulator = ["retroarch"]
        core = ["directxbox_libretro"]
        extensions = ["zip", "iso"]
        if emulator[0] == "retroarch":
            if core[0] == "directxbox_libretro":
                extensions = ["iso"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["xbox"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "directxbox_libretro":
                extensions = ["iso"]

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


class Platform_Microsoft_Msdos(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "dosbox"]
    # cores = ["dosbox_core_libretro", "dosbox_pure_libretro",
    #          "dosbox_svn_libretro", "dosbox_svn_ce_libretro"]
    # extensions = ["zip", "dosz", "exe", "com", "bat", "iso", "cue",
    #               "ins", "img", "ima", "vhd", "jrc", "tc", "m3u", "m3u8"]

    def run(self):
        emulator = ["retroarch"]
        core = ["dosbox_core_libretro"]
        extensions = ["zip", "exe", "com", "bat", "conf"]
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if (
                    core[0] == "dosbox_core_libretro"
                    or core[0] == "dosbox_svn_libretro"
                    or core[0] == "dosbox_svn_ce_libretro"
            ):
                extensions = ["exe", "com", "bat", "conf", "cue", "iso"]
            if core[0] == "dosbox_pure_libretro":
                extensions = ["zip", "dosz", "exe", "com", "bat", "iso", "cue",
                              "ins", "img", "ima", "vhd", "jrc", "tc", "m3u", "m3u8"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "dosbox":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["msdos", "msdosgus", "wild"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if (
                    core[0] == "dosbox_core_libretro"
                    or core[0] == "dosbox_svn_libretro"
                    or core[0] == "dosbox_svn_ce_libretro"
            ):
                extensions = ["exe", "com", "bat", "conf", "cue", "iso"]
            if core[0] == "dosbox_pure_libretro":
                extensions = ["zip", "dosz", "exe", "com", "bat", "iso", "cue",
                              "ins", "img", "ima", "vhd", "jrc", "tc", "m3u", "m3u8"]

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


class Platform_Nec_Pcengine(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["mednafen_supergrafx_libretro", "mednafen_pce_fast_libretro",
    #     "fbneo_pce_libretro", "fbneo_sgx_libretro", "fbneo_tg_libretro"]
    # extensions = ["zip", "pce", "sgx", "cue", "ccd", "chd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mednafen_supergrafx_libretro"]
        extensions = ["zip", "pce", "sgx", "cue", "ccd", "chd"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_supergrafx_libretro":
                extensions = ["pce", "sgx", "cue", "ccd", "chd"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["necturbografxpcengine"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_supergrafx_libretro":
                extensions = ["pce", "sgx", "cue", "ccd", "chd"]

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


class Platform_Nec_Supergrafx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["mednafen_supergrafx_libretro", "mednafen_pce_fast_libretro",
    #          "fbneo_pce_libretro", "fbneo_sgx_libretro", "fbneo_tg_libretro",]
    # extensions = ["zip", "pce", "sgx", "cue", "ccd", "chd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mednafen_supergrafx_libretro"]
        extensions = ["zip", "pce", "sgx", "cue", "ccd", "chd"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_supergrafx_libretro":
                extensions = ["pce", "sgx", "cue", "ccd", "chd"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["necturbografxpcengine"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_supergrafx_libretro":
                extensions = ["pce", "sgx", "cue", "ccd", "chd"]

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


class Platform_Nec_Pc8000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["quasi88_libretro"]
    # extensions = ["zip", "pce", "sgx", "cue", "ccd", "chd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["quasi88_libretro"]
        extensions = ["d88", "u88", "m3u"]
        if emulator[0] == "retroarch":
            if core[0] == "quasi88_libretro":
                extensions = ["d88", "u88", "m3u"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pc8000", "pc8800"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]
        if emulator[0] == "retroarch":
            if core[0] == "quasi88_libretro":
                extensions = ["d88", "u88", "m3u"]

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


class Platform_Nec_Pc8800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["quasi88_libretro"]
    # extensions = ["d88", "u88", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["quasi88_libretro"]
        extensions = ["d88", "u88", "m3u"]
        if emulator[0] == "retroarch":
            if core[0] == "quasi88_libretro":
                extensions = ["d88", "u88", "m3u"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pc8800"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "quasi88_libretro":
                extensions = ["d88", "u88", "m3u"]

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


class Platform_Nec_Pc98(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["nekop2_libretro"]
    # extensions = ["d98", "zip", "98d", "fdi", "fdd", "2hd", "tfd", "d88",
    #               "88d", "hdm", "xdf", "dup", "cmd", "hdi", "thd", "nhd", "hdd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["nekop2_libretro"]
        extensions = ["d98", "zip", "98d", "fdi", "fdd", "2hd", "tfd", "d88",
                      "88d", "hdm", "xdf", "dup", "cmd", "hdi", "thd", "nhd", "hdd"]
        if emulator[0] == "retroarch":
            if core[0] == "nekop2_libretro":
                extensions = ["d98", "zip", "98d", "fdi", "fdd", "2hd", "tfd", "d88",
                              "88d", "hdm", "xdf", "dup", "cmd", "hdi", "thd", "nhd", "hdd"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pc-98"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "nekop2_libretro":
                extensions = ["d98", "zip", "98d", "fdi", "fdd", "2hd", "tfd", "d88",
                              "88d", "hdm", "xdf", "dup", "cmd", "hdi", "thd", "nhd", "hdd"]

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


class Platform_Nec_Pcfx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "other"]
    # cores = ["mednafen_pcfx_libretro"]
    # extensions = ["cue", "ccd", "toc", "chd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mednafen_pcfx_libretro"]
        extensions = ["cue", "ccd", "toc", "chd"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_pcfx_libretro":
                extensions = ["cue", "ccd", "toc", "chd"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pcfx"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == "mednafen_pcfx_libretro":
                extensions = ["cue", "ccd", "toc", "chd"]

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


class Platform_Nintendo_3DS(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    # emulators = ["retroarch", "citra"]
    # cores = ["citra_libretro", "citra2018_libretro", "citra_canary_libretro",
    #          "melonds_libretro", "desmume_libretro", "desmume2015_libretro",]
    # extensions = ["3ds", "3dsx", "elf", "axf", "cci", "cxi", "app"]

    def run(self):
        emulator = ["retroarch"]
        core = ["citra_libretro"]
        extensions = ["3ds", "3dsx", "elf", "axf", "cci", "cxi", "app"]
        if emulator[0] == "retroarch":
            if (
                    core[0] == "citra_libretro"
                    or core[0] == "citra2018_libretro"
                    or core[0] == "citra_canary_libretro"
            ):
                extensions = ["3ds", "3dsx", "elf", "axf", "cci", "cxi", "app"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nintendods"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if (
                    core[0] == "citra_libretro"
                    or core[0] == "citra2018_libretro"
                    or core[0] == "citra_canary_libretro"
            ):
                extensions = ["3ds", "3dsx", "elf", "axf", "cci", "cxi", "app"]

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
    # emulators = ["retroarch", "mupen64plus-glide64",
    #              "mupen64plus-glide64-lle", "mupen64plus-gliden64"]
    # cores = ["mupen64plus_libretro",
    #          "mupen64plus_next_libretro", "parallel_n46_libretro"]
    # extensions = ["n64", "v64", "z64", "bin", "u1", "ndd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mupen64plus_next_libretro"]
        extensions = ["n64", "v64", "z64", "bin", "u1", "ndd"]
        if emulator[0] == "retroarch":
            if core[0] == "mupen64plus_next_libretro":
                extensions = ["n64", "v64", "z64", "bin", "u1", "ndd"]

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
        return ["nintendo64"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ["unknown"]

        if emulator[0] == "retroarch":
            if core[0] == "mupen64plus_next_libretro":
                extensions = ["n64", "v64", "z64", "bin", "u1", "ndd"]

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
        emulator = ["retroarch"]
        core = ["desmume_libretro"]
        extensions = ["zip", "nds", "dsi"]

        if emulator[0] == "retroarch":
            if core[0] == "desmume_libretro":
                extensions = ["nds", "dsi"]

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
        return ["nintendods"]

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == "desmume_libretro":
                extensions = ["nds", "dsi"]

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
    # emulators = ["retroarch", "higan", "emux",
    #              "fceumm", "nestopia", "quicknes", "mesen"]
    # cores = ["quicknes_libretro", "nestopia_libretro", "mess_libretro", "mess2016_libretro",
    #          "mesen_libretro", "fceumm_libretro", "fceumm_mod_libretro", "fbneo_nes_libretro"]
    # extensions = ["zip", "nes", "fds", "unf", "unif", "qd", "nsf"]

    def run(self):
        emulator = ["retroarch"]
        core = ["fceumm_libretro"]
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
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["nesfamicom"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

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
    # emulators = ["retroarch", "other"]
    # cores = ["gambatte_libretro", "mess2016_libretro",
    #          "mess_libretro", "mgba_libretro", "tgbdual_libretro"]
    # extensions = ["zip", "gb", "dmg", "bin", "u1", "ndd", "zip"]

    def run(self):
        emulator = ["retroarch"]
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
        # if len(files) == 0:
        #     # Tries to identify files by any magic necessary.
        #     files = self.find_magic_cookies()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboy"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

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
    # emulators = ["retroarch", "other"]
    # cores = ["gambatte_libretro", "mgba_libretro", "tgbdual_libretro"]
    # extensions = ["zip", "gbc", "dmg", "bin", "u1", "ndd"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mesen-s_libretro"]
        extensions = ["zip", "gbc", "dmg", "bin", "u1", "ndd"]
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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboy", "gameboycolor"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

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
    # emulators = ["retroarch", "other"]
    # cores = ["meteor_libretro", "vba_next_libretro",
    #          "vbam_libretro", "mgba_libretro", "gpsp_libretro"]
    # extensions = ["zip", "gb", "gbc", "gba", "dmg", "agb", "bin", "cgb", "sgb"]

    def run(self):
        emulator = ["retroarch"]
        core = ["vba_next_libretro"]
        extensions = ["zip", "gb", "gbc", "gba",
                      "dmg", "agb", "bin", "cgb", "sgb"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_gba_libretro":
                extensions = ["gba", "agb", "bin"]
            if core[0] == "gpsp_libretro":
                extensions = ["gba", "bin"]
            if core[0] == "meteor_libretro":
                extensions = ["gba"]
            if core[0] == "mgba_libretro":
                extensions = ["gb", "gbc", "gba"]
            if core[0] == "tempgba_libretro":
                extensions = ["gba", "bin", "agb", "gbz"]
            if core[0] == "vbam_libretro":
                extensions = ["dmg", "gb", "gbc", "cgb", "sgb", "gba"]
            if core[0] == "vba_next_libretro":
                extensions = ["gba"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gameboyadvance", "gameboycolor", "gameboy"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_gba_libretro":
                extensions = ["gba", "agb", "bin"]
            if core[0] == "gpsp_libretro":
                extensions = ["gba", "bin"]
            if core[0] == "meteor_libretro":
                extensions = ["gba"]
            if core[0] == "mgba_libretro":
                extensions = ["gb", "gbc", "gba"]
            if core[0] == "tempgba_libretro":
                extensions = ["gba", "bin", "agb", "gbz"]
            if core[0] == "vbam_libretro":
                extensions = ["dmg", "gb", "gbc", "cgb", "sgb", "gba"]
            if core[0] == "vba_next_libretro":
                extensions = ["gba"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["dolphin_libretro"]
    # extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
    #               "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["dolphin_libretro"]
        extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                      "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]
        if emulator[0] == "retroarch":
            if core[0] == "dolphin_libretro":
                extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                              "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["gamecube"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary

    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "dolphin_libretro":
                extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                              "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["pokemini_libretro"]
    # extensions = ["zip", "min"]

    def run(self):
        emulator = ["retroarch"]
        core = ["pokemini_libretro"]
        extensions = ["zip", "min"]
        if emulator[0] == "retroarch":
            if core[0] == "pokemini_libretro":
                extensions = ["min"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["pokemini"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "pokemini_libretro":
                extensions = ["min"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["snes9x_libretro"]
    # extensions = ["zip", "sfc", "smc", "fig", "swc", "bs"]

    def run(self):
        emulator = ["retroarch"]
        core = ["snes9x_libretro"]
        extensions = ["zip", "sfc", "smc", "fig", "swc", "bs"]
        if emulator[0] == "retroarch":
            if (
                    core[0] == "bsnes_libretro"
                    or core[0] == "bsnes_hd_beta_libretro"
                    or core[0] == "bsnes_cplusplus98_libretro"
                    or core[0] == "bsnes2014_accuracy_libretro"
                    or core[0] == "bsnes2014_balanced_libretro"
                    or core[0] == "bsnes2014_performance_libretro"
                    or core[0] == "bsnes_mercury_accuracy_libretro"
                    or core[0] == "bsnes_mercury_balanced_libretro"
                    or core[0] == "bsnes_mercury_balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bs"]
            if (
                    core[0] == "higan_sfc_libretro"
                    or core[0] == "higan_sfc balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bml", "rom"]
            if core[0] == "mesen-s_libretro":
                extensions = ["sfc", "smc", "fig", "swc", "bs", "gb", "gbc"]
            if (
                    core[0] == "snes9x_libretro"
                    or core[0] == "snes9x2002_libretro"
                    or core[0] == "snes9x2005_libretro"
                    or core[0] == "snes9x2005_plus_libretro"
                    or core[0] == "snes9x2010_libretro"
            ):
                extensions = ["smc", "sfc", "swc", "fig", "bs", "st"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["snessuperfamicom"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if (
                    core[0] == "bsnes_libretro"
                    or core[0] == "bsnes_hd_beta_libretro"
                    or core[0] == "bsnes_cplusplus98_libretro"
                    or core[0] == "bsnes2014_accuracy_libretro"
                    or core[0] == "bsnes2014_balanced_libretro"
                    or core[0] == "bsnes2014_performance_libretro"
                    or core[0] == "bsnes_mercury_accuracy_libretro"
                    or core[0] == "bsnes_mercury_balanced_libretro"
                    or core[0] == "bsnes_mercury_balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bs"]
            if (
                    core[0] == "higan_sfc_libretro"
                    or core[0] == "higan_sfc balanced_libretro"
            ):
                extensions = ["sfc", "smc", "gb", "gbc", "bml", "rom"]
            if core[0] == "mesen-s_libretro":
                extensions = ["sfc", "smc", "fig", "swc", "bs", "gb", "gbc"]
            if (
                    core[0] == "snes9x_libretro"
                    or core[0] == "snes9x2002_libretro"
                    or core[0] == "snes9x2005_libretro"
                    or core[0] == "snes9x2005_plus_libretro"
                    or core[0] == "snes9x2010_libretro"
            ):
                extensions = ["smc", "sfc", "swc", "fig", "bs", "st"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["mednafen_vb_libretro"]
    # extensions = ["zip", "vb", "vboy", "bin"]

    def run(self):
        emulator = ["retroarch"]
        core = ["mednafen_vb_libretro"]
        extensions = ["zip", "vb", "vboy", "bin"]
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_vb_libretro":
                extensions = ["vb", "vboy", "bin"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "other":
            print("Using: " + str(emulator))

        # print status to console.
        if DEBUGGING is not False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tSearching for extensions: " + str(extensions))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["virtualboy"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "mednafen_vb_libretro":
                extensions = ["vb", "vboy", "bin"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["dolphin_libretro"]
    # extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
    #               "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

    def run(self):
        emulator = ["retroarch"]
        core = ["dolphin_libretro"]
        extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                      "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

        if emulator[0] == "retroarch":
            if core[0] == "dolphin_libretro":
                extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                              "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["wii", "wiiu", "nintendowii"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "dolphin_libretro":
                extensions = ["gcm", "iso", "wbfs", "ciso", "gcz",
                              "elf", "dol", "dff", "tgc", "wad", "rvz", "m3u"]

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
    # emulators = ['retroarch', 'other']
    # cores = ['mu_libretro']
    # extensions = ['prc', 'pqa', 'img', 'pdb', 'zip']

    def run(self):
        emulator = ["retroarch"]
        core = ['mu_libretro']
        extensions = ['prc', 'pqa', 'img', 'pdb', 'zip']
        if emulator[0] == "retroarch":
            if core[0] == 'mu_libretro':
                extensions = ['prc', 'pqa', 'img', 'pdb', 'zip']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['palmos']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'mu_libretro':
                extensions = ['prc', 'pqa', 'img', 'pdb', 'zip']

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
    # emulators = ["retroarch", "other"]
    # cores = ["4do_libretro", "opera_libretro"]
    # extensions = ["iso", "bin", "chd", "cue"]

    def run(self):
        emulator = ["retroarch"]
        core = ["4do_libretro"]
        extensions = ["iso", "bin", "chd", "cue"]
        if emulator[0] == "retroarch":
            if core[0] == "4do_libretro" or core[0] == "opera_libretro":
                extensions = ["iso", "bin", "chd", "cue"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["3do", "4do"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if (
                core[0] == "4do_libretro"
                or core[0] == "opera_libretro"
            ):
                extensions = ["iso", "bin", "chd", "cue"]
        if emulator[0] == "other":
            extensions = ["unknown"]

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
    # emulators = ["retroarch", "other"]
    # cores = ["samecdi_libretro", "cdi2015_libretro"]
    # extensions = ["zip", "chd", "iso"]

    def run(self):
        emulator = ["retroarch"]
        core = ["samecdi_libretro"]
        extensions = ["zip", "chd", "iso"]
        if emulator[0] == "retroarch":
            if core[0] == "samecdi_libretro":
                extensions = ["chd", "iso"]

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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["palmos"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "samecdi_libretro":
                extensions = ["chd", "iso"]

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
    # emulators = ['retroarch', 'picodrive']
    # cores = ['picodrive_libretro', 'blastem_libretro']
    # extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['picodrive_libretro']
        extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md',
                      '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['sega32x']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

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
    # emulators = ['retroarch', 'flycast', 'redream']
    # cores = ['flycast_libretro', 'flycast_gles2_libretro', 'retrodream_libretro']
    # extensions = ['chd', 'cdi', 'elf', 'bin', 'cue',
    # 			  'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['flycast_libretro']
        extensions = ['chd', 'cdi', 'elf', 'bin', 'cue',
                      'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'flycast_libretro' or core[0] == 'flycast_gles2_libretro':
                extensions = ['chd', 'cdi', 'elf', 'bin', 'cue',
                              'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
            if core[0] == 'retrodream_libretro':
                extensions = ['gdi', 'chd', 'cdi']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['dreamcast']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'flycast_libretro' or core[0] == 'flycast_gles2_libretro':
                extensions = ['chd', 'cdi', 'elf', 'bin', 'cue',
                              'gdi', 'lst', 'zip', 'dat', '7z', 'm3u']
            if core[0] == 'retrodream_libretro':
                extensions = ['gdi', 'chd', 'cdi']

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
    # emulators = ['retroarch', 'osmose']
    # cores = ['gearsystem_libretro',
    #          'genesis_plus_gx_libretro', 'fbneo_gg_libretro']
    # extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

    def run(self):
        emulator = ["retroarch"]
        core = ['genesis_plus_gx_libretro']
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
        if emulator[0] == "retroarch":
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagamegear']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']

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
    # emulators = ['retroarch', 'osmose']
    # cores = ['genesis_plus_gx_libretro', 'fbneo_sms_libretro',
    #          'gearsystem_libretro', 'picodrive_libretro', 'smsplus_gx_libreto']
    # extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
    #               'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['genesis_plus_gx_libretro']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
                      'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        if emulator[0] == "retroarch":
            # MS
            if core[0] == 'emux_sms_libretro':
                extensions = ['sms', 'bms', 'bin', 'rom']
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
            # MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
            # MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segamastersystem', 'segagamegear', 'segasg1000', 'segagenesismegadrive', 'segasaturn', 'segastv']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            # MS
            if core[0] == 'emux_sms_libretro':
                extensions = ['sms', 'bms', 'bin', 'rom']
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
            # MS/GG/SG-1000
            if core[0] == 'gearsystem_libretro':
                extensions = ['sms', 'gg', 'sg', 'bin', 'rom']
            # MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
    # emulators = ['retroarch', 'dgen']
    # cores = ['genesis_plus_gx_libretro',
    #          'fbneo_md_libretro', 'picodrive_libretro']
    # extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
    #               'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['picodrive_libretro']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue',
                      'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        if emulator[0] == "retroarch":
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagenesismegadrive']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            # MS/GG/MD/CD
            if core[0] == 'genesis_plus_gx_libretro' or core[0] == 'genesis_plus_gx_wide_libretro':
                extensions = ['mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                              'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
            # MS/MD/CD/32X
            if core[0] == 'picodrive_libretro':
                extensions = ['bin', 'gen', 'gg', 'smd', 'pco', 'md',
                              '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']

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
    # emulators = ['retroarch', 'yabause', 'kronos']
    # cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    # extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

    def run(self):
        emulator = ["retroarch"]
        core = ['yabause_libretro']
        extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasaturn']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']

        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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
    # emulators = ['retroarch', 'yabause', 'kronos']
    # cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    # extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['kronos_libretro']
        extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segastv']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_saturn_libretro':
                extensions = ['ccd', 'chd', 'cue', 'toc', 'm3u']
            if core[0] == 'kronos_libretro':
                extensions = ['ccd', 'chd', 'cue', 'iso', 'mds', 'zip', 'm3u']
            if core[0] == 'yabause_libretro' or core[0] == 'yabasanshiro_libretro':
                extensions = ['bin', 'ccd', 'chd', 'cue', 'iso', 'mds', 'zip']

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
    # emulators = ['retroarch', 'vemulator']
    # cores = ['vemulator_libretro']
    # extensions = ['zip', 'vms', 'dci', 'bin']

    def run(self):
        emulator = ["retroarch"]
        core = ['vemulator_libretro']
        extensions = ['zip', 'vms', 'dci', 'bin']
        if emulator[0] == "retroarch":
            if core[0] == 'vemulator_libretro':
                extensions = ['vms', 'dci', 'bin']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segavmu']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "other":
            extensions = ['unknown']
        if emulator[0] == "retroarch":
            if core[0] == 'vemulator_libretro':
                extensions = ['vms', 'dci', 'bin']

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
    # emulators = ['retroarch', 'gearsystem']
    # cores = ['gearsystem_libretro', 'bluemsx_libretro']
    # extensions = ['rom', 'ri', 'mx1', 'mx2',
    #               'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['bluemsx_libretro']
        extensions = ['rom', 'ri', 'mx1', 'mx2',
                      'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
        if emulator[0] == "retroarch":
            # MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasg1000']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            # MSX/SVI/ColecoVision/SG-1000
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
    # emulators = ["retroarch"]
    # cores = ["fuse_libretro", "81_libretro"]
    # extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk"]

    def run(self):
        emulator = ["retroarch"]
        core = ["fuse_libretro", "81_libretro"]
        extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk", "zip"]
        if emulator[0] == "retroarch":
            if core[0] == "fuse_libretro":
                extensions = ["tzx", "tap", "z80",
                              "rzx", "scl", "trd", "dsk", "zip"]
            if core[0] == "81_libretro":
                extensions = ["tzx", "tap", "z80",
                              "rzx", "scl", "trd", "dsk", "zip"]
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
        if emulator[0] == "retroarch":
            emulator.append("-L")
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["zxenhanced", "spectrum", "zxspectrum"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "fuse_libretro":
                extensions = ["tzx", "tap", "z80",
                              "rzx", "scl", "trd", "dsk", "zip"]

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
    # emulators = ["retroarch", "81"]
    # cores = ["fuse_libretro", "81_libretro"]
    # extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk"]

    def run(self):
        emulator = ["retroarch"]
        core = ["81_libretro"]
        extensions = ["tzx", "tap", "z80", "rzx", "scl", "trd", "dsk"]
        if emulator[0] == "retroarch":
            if core[0] == "fuse_libretro":
                extensions = ["tzx", "tap", "z80",
                              "rzx", "scl", "trd", "dsk", "zip"]
            if core[0] == "81_libretro":
                extensions = ["p", "tzx", "t81"]

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
        if emulator[0] == "retroarch":
            print("Using:" + str(emulator))
            emulator.append("-L")
            emulator.append(core[0])
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "other":
            print("Using:" + str(emulator))

        # print status to console.
        if DEBUGGING is not False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tSearching for extensions: " + str(extensions))

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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "3do":
                emulator = emulator + ["-flipname", flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ["zx81"]

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == "fuse_libretro":
                extensions = ["tzx", "tap", "z80",
                              "rzx", "scl", "trd", "dsk", "zip"]
            if core[0] == "81_libretro":
                extensions = ["p", "tzx", "t81"]

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
    # emulators = ['retroarch', 'other']
    # cores = ['fbneo_libretro', 'neocd_libretro', 'fbalpha2012_libretro']
    # extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
        emulator = ["retroarch"]
        core = ['mednafen_ngp_libretro']
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeo']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
    # emulators = ['retroarch', 'other']
    # cores = ['mednafen_ngp_libretro', 'fbneo_ngp']
    # extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
        emulator = ["retroarch"]
        core = ['mednafen_ngp_libretro']
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeopocket']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
    # emulators = ['retroarch', 'other']
    # cores = ['mednafen_ngp_libretro', 'fbneo_ngpc']
    # extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']

    def run(self):
        emulator = ["retroarch"]
        core = ['mednafen_ngp_libretro']
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['neogeopocketcolor']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):

        if emulator[0] == "retroarch":
            if core[0] == 'mednafen_ngp_libretro':
                extensions = ['ngp', 'ngc', 'ngpc', 'npc']

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
    # emulators = ['retroarch', 'other']
    # cores = ['pcsx2_libretro', 'play_libretro']
    # extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img',
    #               'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['pcsx2_libretro']
        extensions = ['zip', 'exe', 'psexe', 'cue', 'toc', 'bin', 'img',
                      'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'pcsx2_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img',
                              'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'play_libretro':
                extensions = ['chd', 'cso', 'cue', 'elf', 'iso', 'isz']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstation2']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'pcsx2_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img',
                              'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'play_libretro':
                extensions = ['chd', 'cso', 'cue', 'elf', 'iso', 'isz']

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
    # emulators = ['retroarch', 'ppsspp']
    # cores = ['ppsspp_libretro']
    # extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

    def run(self):
        emulator = ["retroarch"]
        core = ['ppsspp_libretro']
        extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
        if emulator[0] == "retroarch":
            if core[0] == 'ppsspp_libretro':
                extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == "other":
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstationportable']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'ppsspp_libretro':
                extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']

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
    # emulators = ['retroarch', 'other']
    # cores = ['pcsx_rearmed_libretro',
    # 		 'mednafen_psx_libretro', 'swanstation_libretro']
    # extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img',
    # 			  'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['swanstation_libretro']
        extensions = ['zip', 'exe', 'psx', 'psexe', 'cue', 'toc', 'bin', 'img',
                      'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'duckstation_libretro' or core[0] == 'swanstation_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img',
                              'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'rustation_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe']
            if core[0] == 'mednafen_psx_libretro' or core[0] == 'mednafen_psx_hw_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe', 'pbp', 'chd']
            if core[0] == 'pcsx1_libretro':
                extensions = ['bin', 'cue', 'img',
                              'mdf', 'pbp', 'toc', 'cbn', 'm3u']
            if core[0] == 'pcsx_rearmed_libretro' or core[0] == 'pcsx_rearmed_neon_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf',
                              'pbp', 'toc', 'cbn', 'm3u', 'ccd', 'chd']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['playstation']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'duckstation_libretro' or core[0] == 'swanstation_libretro':
                extensions = ['exe', 'psexe', 'cue', 'bin', 'img',
                              'iso', 'chd', 'pbp', 'ecm', 'mds', 'psf', 'm3u']
            if core[0] == 'rustation_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe']
            if core[0] == 'mednafen_psx_libretro' or core[0] == 'mednafen_psx_hw_libretro':
                extensions = ['cue', 'toc', 'm3u', 'ccd', 'exe', 'pbp', 'chd']
            if core[0] == 'pcsx1_libretro':
                extensions = ['bin', 'cue', 'img',
                              'mdf', 'pbp', 'toc', 'cbn', 'm3u']
            if core[0] == 'pcsx_rearmed_libretro' or core[0] == 'pcsx_rearmed_neon_libretro':
                extensions = ['bin', 'cue', 'img', 'mdf',
                              'pbp', 'toc', 'cbn', 'm3u', 'ccd', 'chd']

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
    # emulators = ['retroarch', 'other']
    # cores = ['bluemsx_libretro']
    # extensions = ['rom', 'ri', 'mx1', 'mx2',
    # 			  'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

    def run(self):
        emulator = ["retroarch"]
        core = ['bluemsx_libretro']
        extensions = ['rom', 'ri', 'mx1', 'mx2',
                      'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']
        if emulator[0] == "retroarch":
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['spectravision']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'bluemsx_libretro':
                extensions = ['rom', 'ri', 'mx1', 'mx2',
                              'col', 'dsk', 'cas', 'sg', 'sc', 'm3u']

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
    # emulators = ['retroarch', 'other']
    # cores = ['theodore_libretro']
    # extensions = ['fd', 'sap', 'k7', 'm7', 'm5', 'rom']

    def run(self):
        emulator = ["retroarch"]
        core = ['theodore_libretro']
        extensions = ['fd', 'sap', 'k7', 'm7', 'm5', 'rom']
        if emulator[0] == "retroarch":
            if core[0] == 'theodore_libretro':
                extensions = ['fd', 'sap', 'k7', 'm7', 'm5', 'rom']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['thomson']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'theodore_libretro':
                extensions = ['fd', 'sap', 'k7', 'm7', 'm5', 'rom']

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
    # emulators = ['retroarch', 'other']
    # cores = ['gme_libretro']
    # extensions = ['zip', 'ay', 'gbs', 'gym', 'hes',
    # 			  'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']

    def run(self):
        emulator = ["retroarch"]
        core = ['gme_libretro']
        extensions = ['zip', 'ay', 'gbs', 'gym', 'hes',
                      'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
        if emulator[0] == "retroarch":
            if core[0] == 'gme_libretro':
                extensions = ['ay', 'gbs', 'gym', 'hes', 'kss',
                              'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz', 'zip']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'music']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'gme_libretro':
                extensions = ['ay', 'gbs', 'gym', 'hes', 'kss',
                              'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz', 'zip']

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
    # emulators = ['retroarch', 'other']
    # cores = ['ffmpeg_libretro']
    # extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
    #               '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
        emulator = ["retroarch"]
        core = ['ffmpeg_libretro']
        extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                      '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        if emulator[0] == "retroarch":
            if core[0] == 'ffmpeg_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                              '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'ffmpeg_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                              '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

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
    # emulators = ['retroarch', 'other']
    # cores = ['mpv_libretro']
    # extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
    #               '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
        emulator = ["retroarch"]
        core = ['mpv_libretro']
        extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                      '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        if emulator[0] == "retroarch":
            if core[0] == 'mpv_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                              '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

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
        if emulator[0] == "retroarch":
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
            if emulator[0] == "retroarch":
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

            # if not os.path.exists(self.datadir + "/s"):
            #     os.makedirs(self.datadir + "/s")
            #     # when find_files_with_extension works with paths relative to datadir.
            #     # we can simplify this
            #     with open(self.datadir + "/s/startup-sequence", 'w') as f:
            #         exename = files[0].split('/')
            #         exename = exename[len(exename) - 1]
            #         f.write(exename + "\n")
            #         f.close()

        # if emulator[0] == "retroarch":
        #     amiga_model = 'A1200'
        #     if self.prod_platform == 'amigaocsecs':
        #         amiga_model = 'A500'
        #     # if self.prod_platform == 'amigaaga':
        #     #     emulator.append('--fast_memory=8192')
        #     if len(drives) > 0:
        #         print("\tUsing drive 0: ", drives[0])
        #         emulator.append(drives[0])
        #     if len(drives) > 1:
        #         print("\tUsing drive 1: ", drives[1])
        #         emulator.append(drives[1])
        #     if len(drives) > 2:
        #         print("\tUsing drive 2: ", drives[2])
        #         emulator.append(drives[2])
        #     if len(drives) > 3:
        #         print("\tUsing drive 3: ", drives[3])
        #         emulator.append(drives[3])
        # emulator.append('--model=' + amiga_model)

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

    # Search demo files for amiga magic cookie (executable file)
    # def find_magic_cookies(self):
    #     cookie_files = []
    #     for file in self.prod_files:
    #         with open(file, "rb") as fin:
    #             header = fin.read(4)
    #             if len(header) == 4:
    #                 # Signature for Amiga magic cookie
    #                 if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
    #                     cookie_files.append(file)
    #     return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self, emulator, core):
        if emulator[0] == "retroarch":
            if core[0] == 'mpv_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm',
                              '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

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
