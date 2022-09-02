from platformcommon import PlatformCommon
import os.path

fullscreen = ['false']


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
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('directxbox_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("Using: " + emulator)

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
        return ['xbox']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)

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
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('bluemsx_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("Using: " + emulator)

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
        return ['msx', 'msx2', 'msx2plus', 'msxturbor', 'spectravideo3x8']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)

        return ext_files

 # Tries to identify files by any magic necessary

    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)

        return ext_files


class PlatformWindows(PlatformCommon):
    def run(self):
        extensions = ['exe']
        emulator = ['wine']

        wineprefix = self.showetdir + '/wineprefix'
        for ext in extensions:
            exes = self.find_files_with_extension(ext)

        if len(exes) == 0:
            print("Didn't find any exe files.")
            exit(-1)

        print("Using: " + emulator)

        exefile = exes[0]

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
        return ['windows', 'java']

    # Tries to identify files by any magic necessary
    # def find_ext_files(self):
    #     ext_files = []
    #     for file in self.prod_files:
    #         size = os.path.getsize(file)
    #         if size > 0:
    #             if not file.endswith('.json'):
    #                 ext_files.append(file)
    #                 print("Found file: " + file)

    #     return ext_files
