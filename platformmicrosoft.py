import os.path
from platformcommon import PlatformCommon

emulators = ['wine', 'retroarch']
cores = ['directxbox_libretro']
fullscreens = ['false']


class PlatformXbox(PlatformCommon):
    def run(self):
        extensions = ['iso']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['directxbox_libretro']
        fullscreen = ['false']

        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append('directxbox_libretro')
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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['xbox']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformMsx(PlatformCommon):
    def run(self):
        extensions = ['rom', 'ri', 'mx1', 'mx2', 'col',
                      'dsk', 'fdi', 'cas', 'sg', 'sc', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['bluemsx_libretro']
        fullscreen = ['false']

        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append('bleumsx_libretro')
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
            if emulator == 'retroarch':
                emulator = emulator + [files[0]]
        self.run_process(emulator)

    def supported_platforms(self):
        return ['msx', 'msx2', 'msx2plus', 'msxturbor', 'spectravideo3x8']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformWindows(PlatformCommon):
    def run(self):
        extensions = ['exe', 'bat']
        emulator = ['wine']
        core = ['wine']
        fullscreen = ['false']
        wineprefix = self.showetdir + '/wineprefix'

        for ext in extensions:
            exes = self.find_files_with_extension(ext)

        if len(exes) == 0:
            print("Didn't find any exe files.")
            exit(-1)

        exefile = exes[0]

        print("\tUsing emulator: " + str(emulator))
        print("\tUsing core: " + str(core))
        print("\tUsing fullscreen: " + str(fullscreen))

        print("Guessed executable file: " + exefile)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed
        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win64" winecfg')
        self.run_process([emulator, exefile])

    def supported_platforms(self):
        return ['windows', 'java', 'javascript']

    # Tries to identify files by any magic necessary
    # def find_ext_files(self):
    #     ext_files = []
    #     for file in self.prod_files:
    #         size = os.path.getsize(file)
    #         if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
    #                 ext_files.append(file)
    #                 print("\tFound file: " + file)
    #     return ext_files
