import os
import os.path
from platformcommon import PlatformCommon

class Platform_STETTFalcon(PlatformCommon):
    emulators = ['retroarch', 'stella']
    cores = ['hatari_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['hatari_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'st', 'msa', 'zip',
                      'stx', 'dim', 'ipf', 'm3u']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['hatari_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('hatari_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarifalcon030', 'atarist', 'atariste']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Atarixlxe(PlatformCommon):
    emulators = ['retroarch']
    cores = ['atari800_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['atari800_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['st', 'msa', 'zip', 'stx',
                      'dim', 'ipf', 'm3u', 'xex']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['atari800_libretro']
        fullscreen = ['false']

        if emulator[0] == ['retroarch']:
            emulator.append('-L')
            emulator.append('atari800_libretro')
            if fullscreen == 'true':
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Jaguar(PlatformCommon):
    emulators = ['retroarch']
    cores = ['virtualjaguar_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['virtualjaguar_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'j64', 'jag', 'rom',
                      'abs', 'cof', 'bin', 'prg']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['virtualjaguar_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('virtualjaguar_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijaguar']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Lynx(PlatformCommon):
    emulators = ['retroarch', 'mednafen']
    cores = ['handy_libretro', 'mednafen_lynx_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mednafen_lynx_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['lnx', 'o']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mednafen_lynx_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_lynx_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarilynx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_2600(PlatformCommon):
    emulators = ['retroarch', 'stella']
    cores = ['stella2014_libretro', 'stella_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['stella2014_libretro', 'stella_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'a26', 'bin']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['stella2014_libretro', 'stella_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('stella2014_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarivcs']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_5200(PlatformCommon):
    emulators = ['retroarch', 'atari800']
    cores = ['atari800_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['atari800_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'zip', 'atx', 'car', 'rom', 'com', 'xex']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['atari800_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('atari800_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_5200(PlatformCommon):
    emulators = ['retroarch', 'prosystem']
    cores = ['prosystem_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['prosystem_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['a78', 'bin', 'cdf']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        # if len(files) == 0:
        #      files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['prosystem_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('prosystem_libretro')
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
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atari7800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        exclusions = ['json', 'txt', 'nfo', 'doc', 'me']
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                #if not file.endswith(str(exclusions)) and not file.endswith(str(exclusions).upper()):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files

