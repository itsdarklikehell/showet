import os
from platformcommon import PlatformCommon

emulators = ['retroarch']
cores = ['quicknes_libretro']
fullscreens = ['false']


class PlatformFamicom(PlatformCommon):
    def run(self):
        extensions = ['nes', 'fds', 'unf', 'unif', 'qd', 'nsf']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['quicknes_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('quicknes_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['nesfamicom']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformSuperFamicom(PlatformCommon):
    def run(self):
        extensions = ['sfc', 'smc', 'fig', 'swc', 'bs']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['snes9x_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('snes9x_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['snessuperfamicom']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformN64(PlatformCommon):
    def run(self):
        extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mupen64plus_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mupen64plus_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['nintendo64']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformGameboy(PlatformCommon):
    def run(self):
        extensions = ['gb', 'dmg', 'bin', 'u1', 'ndd', 'zip']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['gambatte_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gambatte_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['gameboy']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformGameboyColor(PlatformCommon):
    def run(self):
        extensions = ['gbc', 'dmg', 'bin', 'u1', 'ndd']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['gambatte_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gambatte_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['gameboy', 'gameboycolor']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformGameboyAdvance(PlatformCommon):
    def run(self):
        extensions = ['gb', 'gbc', 'gba', 'dmg', 'agb', 'bin', 'cgb', 'sgb']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vba_next_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vba_next_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['gameboyadvance', 'gameboycolor', 'gameboy']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformGamecube(PlatformCommon):
    def run(self):
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['dolphin_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('dolphin_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['gamecube']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformWii(PlatformCommon):
    def run(self):
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['dolphin_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('dolphin_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['wii', 'wiiu']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformPokemini(PlatformCommon):
    def run(self):
        extensions = ['min']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['pokemini_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('pokemini_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['pokemini']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformDS(PlatformCommon):
    def run(self):
        extensions = ['nds', 'dsi']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['melonds_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('melnonds_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['nintendods']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformVirtualboy(PlatformCommon):
    def run(self):
        extensions = ['vb', 'vboy', 'bin']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mednafen_vb_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_vb_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

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
        return ['virtualboy']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
