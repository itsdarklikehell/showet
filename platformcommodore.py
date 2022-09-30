import os
from platformcommon import PlatformCommon


class PlatformCommodore64(PlatformCommon):
    emulators = ['retroarch']
    cores = ['vice_x64_libretro']
    fullscreens = ['false']

    emulator = ['retroarch', 'vice-x64']
    core = ['vice_x64_libretro']
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
        core = ['vice_x64_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x64_libretro')
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodorePet(PlatformCommon):
    emulators = ['retroarch']
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
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodore128(PlatformCommon):
    emulators = ['retroarch']
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
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodorePlus4(PlatformCommon):
    emulators = ['retroarch']
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
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodoreCBM(PlatformCommon):
    emulators = ['retroarch']
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
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodoreVIC20(PlatformCommon):
    emulators = ['retroarch']
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
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
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
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files

