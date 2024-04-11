import os
import stat
import os.path

from platformcommon import PlatformCommon

FULLSCREEN = False
DEBUGGING = True


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
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == "other":
            # Set whether we should run in fullscreens or not.
            if FULLSCREEN is True:
                emulator.append('--fullscreen')

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
