import os
import stat
import os.path

from platformcommon import PlatformCommon

FULLSCREEN = False
DEBUGGING = True


class Platform_SuperFamicom(PlatformCommon):
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