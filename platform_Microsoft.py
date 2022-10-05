import os
import os.path
from platformcommon import PlatformCommon

class Platform_Xbox(PlatformCommon):
    emulators = ['retroarch']
    cores = ['directxbox_libretro']
    fullscreens = ['false']

    # emulator = ['retroarch']
    # core = ['directxbox_libretro']
    # fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'iso']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['directxbox_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('directxbox_libretro')
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
        return ['xbox']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') or file.endswith('.txt') or file.endswith('.diz') or file.endswith('.png'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_Msx(PlatformCommon):
    emulators = ['retroarch', 'openmsx', 'openmsx-msx2',
                 'openmsx-msx2-plus', 'openmsx-msx-turbo']
    cores = ['bluemsx_libretro', 'fbneo_msx_libretro', 'fmsx_libretro']
    fullscreens = ['false']

    # emulator = ['retroarch']
    # core = ['fmsx_libretro']
    # fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'rom', 'ri', 'mx1',
                      'mx2', 'col', 'dsk', 'fdi',
                      'cas', 'sg', 'sc', 'm3u']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['fmsx_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('fmsx_libretro')
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
        return ['msx', 'msx2', 'msx2plus', 'msxturbor', 'spectravideo3x8']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') or file.endswith('.txt') or file.endswith('.diz') or file.endswith('.png'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class Platform_Windows(PlatformCommon):
    emulators = ['wine']
    cores = ['wine']
    fullscreens = ['false']

    # emulator = ['wine']
    # core = ['wine']
    # fullscreen = ['false']

    def run(self):
        extensions = ['exe', 'bat', 'com']
        emulator = ['wine']
        core = ['wine']
        fullscreen = ['false']
        wineprefix = self.showetdir + '/wineprefix'

        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        exefile = files[0]

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

        print("Guessed executable file: " + exefile)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed
        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win64" winecfg')
        self.run_process([emulator[0], exefile])

    def supported_platforms(self):
        return ['windows', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if file.endswith('.exe') or file.endswith('.bat') or file.endswith('.com'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files