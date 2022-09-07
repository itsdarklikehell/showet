from platformcommon import PlatformCommon
import os

emulator = ['retroarch']
fullscreen = ['false']


class PlatformFalcon(PlatformCommon):
    def run(self):
        extensions = ['st', 'dim', 'msa', 'stx',
                      'ipf', 'm3u', 'vsf', 'm3u', 'zip']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('hatari_libretro')
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarifalcon030']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformAtarist(PlatformCommon):
    def run(self):
        extensions = ['st', 'msa', 'stx', 'ipf', 'm3u', 'vsf', 'm3u', 'zip']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('hatari_libretro')
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarist', 'atariste']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformAtarixlxe(PlatformCommon):
    def run(self):
        extensions = ['zip', 'xfd', 'atr', 'xfdx', 'cdm',
                      'cas', 'bin', 'a52', 'xex', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == ['retroarch']:
            emulator.append('-L')
            emulator.append('hatari_libretro')
            if fullscreen == 'true':
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformJaguar(PlatformCommon):
    def run(self):
        extensions = ['j64', 'jag', 'rom', 'abs',
                      'cof', 'bin', 'prg']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('virtualjaguar_libretro')
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijaguar']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformLynx(PlatformCommon):
    def run(self):
        extensions = ['lnx', 'o', 'm3u', 'zip']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('handy_libretro')
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijlynx']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformVcs(PlatformCommon):
    def run(self):
        extensions = ['a26', 'bin']
        for ext in extensions:
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator[0] = ['retroarch']
        fullscreen[0] = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('stella_libretro')
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
                emulator[0] = emulator[0] + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarivcs']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):

                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
