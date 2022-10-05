import os
import os.path
from platformcommon import PlatformCommon

class Platform_Commodore64(PlatformCommon):
    emulators = ['retroarch', 'vice', 'frodo']
    cores = ['vice_x64sc_libretro', 'frodo_libretro']
    fullscreens = ['false']

    emulator = ['retroarch', 'vice-x64']
    core = ['vice_x64sc_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
            
        if len(files) == 0:
            files = self.find_ext_files()
            
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vice_x64sc_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x64sc_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
                
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
                
        if len(files) > 0:
            files = self.sort_disks(files)
            
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
                
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore64']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_Commodore128(PlatformCommon):
    emulators = ['retroarch', 'vice']
    cores = ['vice_x128_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['vice_x128_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vice_x128_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x128_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore128']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_CommodoreAmiga(PlatformCommon):
    emulators = ['retroarch', 'puae', 'fs-uae']
    cores = ['puae2021_libretro', 'puae_libretro', 'fsuae_libretro', 'uae4arm_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['puae_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'm3u', 'adf', 'adz',
                      'dms', 'fdi', 'ipf', 'hdf',
                      'hdz', 'lha', 'tga', 'slave',
                      'info', 'cue', 'ccd', 'nrg',
                      'mds', 'iso', 'chd', 'uae',
                      '7z', 'rp9', 'exe', 'run']

        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['puae_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('puae_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')
        if emulator[0] == 'fs-uae':
            if fullscreen != 'false':
                emulator.append('--fullscreen')
                emulator.append('--keep_aspect')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        drives = []
        # Support only one for now..
        if len(files) > 0:
            if emulator[0] == 'fs-uae':
                emulator.append('--hard_drive_0=.')
            if emulator[0] == 'retroarch':
                # emulator.append('--hard_drive_0=.')
                emulator = emulator + [files[0]]
            if not os.path.exists(self.datadir + "/s"):
                os.makedirs(self.datadir + "/s")
                # when find_files_with_extension works with paths relative to datadir.
                # we can simplify this
                with open(self.datadir + "/s/startup-sequence", 'w') as f:
                    exename = files[0].split('/')
                    exename = exename[len(exename) - 1]
                    f.write(exename + "\n")
                    f.close()
        if len(files) > 0:
            drives = self.sort_disks(files)
            emulator = emulator + [files[0]]

        if emulator[0] == 'fs-uae':
            amiga_model = 'A1200'
            if self.prod_platform == 'amigaocsecs':
                amiga_model = 'A500'
                
            if self.prod_platform == 'amigaaga':
                emulator.append('--fast_memory=8192')
                
            if len(drives) > 0:
                print("\tUsing drive 0: ", drives[0])
                emulator.append('--floppy_drive_0=' + drives[0])
            if len(drives) > 1:
                print("\tUsing drive 1: ", drives[1])
                emulator.append('--floppy_drive_1=' + drives[1])
            if len(drives) > 2:
                print("\tUsing drive 2: ", drives[2])
                emulator.append('--floppy_drive_2=' + drives[2])
            if len(drives) > 3:
                print("\tUsing drive 3: ", drives[3])
                emulator.append('--floppy_drive_3=' + drives[3])
            emulator.append('--model=' + amiga_model)

        if emulator[0] == 'retroarch':
            amiga_model = 'A1200'
            if self.prod_platform == 'amigaocsecs':
                amiga_model = 'A500'
                
            # if self.prod_platform == 'amigaaga':
            #     emulator.append('--fast_memory=8192')
                
            if len(drives) > 0:
                print("\tUsing drive 0: ", drives[0])
                emulator.append(drives[0])
            if len(drives) > 1:
                print("\tUsing drive 1: ", drives[1])
                emulator.append(drives[1])
            if len(drives) > 2:
                print("\tUsing drive 2: ", drives[2])
                emulator.append(drives[2])
            if len(drives) > 3:
                print("\tUsing drive 3: ", drives[3])
                emulator.append(drives[3])
            #emulator.append('--model=' + amiga_model)
        self.run_process(emulator)

    def supported_platforms(self):
        return ['amigaocsecs', 'amigaaga', 'amigappcrtg']

    # Search demo files for amiga magic cookie (executable file)
    def find_magic_cookies(self):
        cookie_files = []
        for file in self.prod_files:
            with open(file, "rb") as fin:
                header = fin.read(4)
                if len(header) == 4:
                    # Signature for Amiga magic cookie
                    if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
                        cookie_files.append(file)
        return cookie_files

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_CommodoreCBMII(PlatformCommon):
    emulators = ['retroarch', 'vice']
    cores = ['vice_xcbm2_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['vice_xcbm2_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vice_xcbm2_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xcbm2_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodorecbm']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_CommodorePet(PlatformCommon):
    emulators = ['retroarch', 'vice']
    cores = ['vice_xpet_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['vice_xpet_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vice_xpet_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xpet_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodorepet']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_CommodorePlus4(PlatformCommon):
    emulators = ['retroarch', 'vice']
    cores = ['vice_xplus4_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['vice_xplus4_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['vice_xplus4_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xplus4_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodoreplus4', 'c16116plus4']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_CommodoreVIC20(PlatformCommon):
    emulators = ['retroarch', 'vice']
    cores = ['vice_xvic_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['vice_xvic_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'd64', 'd71', 'd80',
                      'd81', 'd82', 'g64', 'g41',
                      'x64', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'gz',
                      'd6z', 'd7z', 'd8z', 'g6z',
                      'g4z', 'x6z', 'cmd', 'm3u',
                      'vfl', 'vsf', 'nib', 'nbz',
                      'd2m', 'd4m', '20', '40',
                      '60', 'a0', 'b0', 'rom']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vice_xvic_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xvic_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['vic20']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['asm', 'json', 'txt', 'nfo', 'doc', 'me', 'pcx', 'diz']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('diz') and not file.endswith('jpg'):
                #    if not file.endswith(str(exclusions)):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
