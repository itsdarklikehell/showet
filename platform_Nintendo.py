import os
import os.path
from platformcommon import PlatformCommon

class Platform_3DS(PlatformCommon):
    emulators = ['retroarch', 'citra']
    fullscreens = ['false']
    cores = ['melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['melonds_libretro']

    def run(self):
        extensions = ['zip', 'nds', 'dsi']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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
            emulator.append('melonds_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_N64(PlatformCommon):
    emulators = ['retroarch', 'mupen64plus-glide64',
                 'mupen64plus-glide64-lle', 'mupen64plus-gliden64']
    cores = ['mupen64plus_libretro',
             'mupen64plus_next_libretro', 'parallel_n46_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mupen64plus_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_DS(PlatformCommon):
    emulators = ['retroarch', 'desmume', 'melonds']
    fullscreens = ['false']
    cores = ['melonds_libretro', 'desmume_libretro', 'desmume2015_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['desmume_libretro']

    def run(self):
        extensions = ['zip', 'nds', 'dsi']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['desmume_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('desmume_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Famicom(PlatformCommon):
    emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
    cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro',
             'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['fceumm_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'nes', 'fds', 'unf',
                      'unif', 'qd', 'nsf']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_FamicomDisksystem(PlatformCommon):
    emulators = ['retroarch', 'higan', 'emux', 'fceumm', 'nestopia', 'quicknes', 'mesen']
    cores = ['quicknes_libretro', 'nestopia_libretro', 'mess_libretro', 'mess2016_libretro',
             'mesen_libretro', 'fceumm_libretro', 'fceumm_mod_libretro', 'fbneo_nes_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['fceumm_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'nes', 'fds', 'unf',
                      'unif', 'qd', 'nsf']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Gameboy(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['gambatte_libretro', 'mess2016_libretro',
             'mess_libretro', 'mgba_libretro', 'tgbdual_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['gambatte_libretro']

    def run(self):
        extensions = ['zip', 'gb', 'dmg', 'bin', 'u1', 'ndd', 'zip']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_GameboyColor(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['gambatte_libretro', 'mgba_libretro', 'tgbdual_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['gambatte_libretro']

    def run(self):
        extensions = ['zip', 'gbc', 'dmg', 'bin', 'u1', 'ndd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_GameboyAdvance(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['vba_next_libretro', 'mgba_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['vba_next_libretro']

    def run(self):
        extensions = ['zip', 'gb', 'gbc', 'gba',
                      'dmg', 'agb', 'bin', 'cgb', 'sgb']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Gamecube(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['dolphin_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['dolphin_libretro']

    def run(self):
        extensions = ['zip', 'gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Pokemini(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['pokemini_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['pokemini_libretro']

    def run(self):
        extensions = ['zip', 'min']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_SuperFamicom(PlatformCommon):
    emulators = ['retroarch']
    cores = ['snes9x_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['snes9x_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'sfc', 'smc', 'fig', 'swc', 'bs']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Virtualboy(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['mednafen_vb_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['mednafen_vb_libretro']

    def run(self):
        extensions = ['zip', 'vb', 'vboy', 'bin']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Wii(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['dolphin_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['dolphin_libretro']

    def run(self):
        extensions = ['zip', 'gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        #if len(files) == 0:
        #     files = self.find_files_with_extension(ext.upper())
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

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        # flipfile = self.datadir + "/fliplist.vfl"
        # m3ufile = self.datadir + "/fliplist.m3u"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")
        # with open(m3ufile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in files:
        #         f.write(disk + "\n")

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
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files

