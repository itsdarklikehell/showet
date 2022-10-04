import os
import os.path
from platformcommon import PlatformCommon

class Platform_Zxspectrum(PlatformCommon):
    emulators = ['retroarch', '81']
    cores = ['fuse_libretro', '81_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['fuse_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['tzx', 'p', 't81',
                      'tap', 'z80', 'rzx', 'scl',
                      'trd', 'dsk', 'zip']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
             files = self.find_files_with_extension(ext.upper())
        elif len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['fuse_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('fuse_libretro')
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
        return ['zxspectrum', 'zxenhanced', 'spectrum']

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


class Platform_Zx81(PlatformCommon):
    emulators = ['retroarch', '81']
    cores = ['fuse_libretro', '81_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['81_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['tzx', 'p', 't81',
                      'tap', 'z80', 'rzx', 'scl',
                      'trd', 'dsk', 'zip']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
             files = self.find_files_with_extension(ext.upper())
        elif len(files) == 0:
            files = self.find_ext_files()
        elif len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['81_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core)
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
        return ['zx81']

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

