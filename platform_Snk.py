import os
import os.path
from platformcommon import PlatformCommon

class Platform_Neogeo(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['fbneo_libretro', 'neocd_libretro', 'fbalpha2012_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['fbneo_libretro']

    def run(self):
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
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
        core = ['mednafen_ngp_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_ngp_libretro')
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
        return ['neogeo']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Neopocket(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['mednafen_ngp_libretro', 'fbneo_ngp']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['mednafen_ngp_libretro']

    def run(self):
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
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
        core = ['mednafen_ngp_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_ngp_libretro')
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
        return ['neogeopocket']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class Platform_Neopocketcolor(PlatformCommon):
    emulators = ['retroarch']
    fullscreens = ['false']
    cores = ['mednafen_ngpc_libretro', 'fbneo_ngpc']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['mednafen_ngpc_libretro']

    def run(self):
        extensions = ['zip', 'ngp', 'ngc', 'ngpc', 'npc']
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
        core = ['mednafen_ngpc_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_ngpc_libretro')
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
        return ['neogeopocketcolor']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


