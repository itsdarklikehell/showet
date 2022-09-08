import os
from platformcommon import PlatformCommon


fullscreen = ['false']
emulator = ['retroarch']


class PlatformCommodore64(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x64_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodorePet(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xpet_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodore128(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x128_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodorePlus4(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xplus4_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
        return ['commodoreplus4']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodoreCBM(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xcbm2_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformCommodoreVIC20(PlatformCommon):

    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_xvic_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])

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
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
