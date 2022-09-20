import os
from platformcommon import PlatformCommon

emulators = ['retroarch']
core = ['mednafen_psx_libretro']
fullscreens = ['false']


class PlatformPsx(PlatformCommon):
    def run(self):
        extensions = ['exe', 'psexe', 'cue', 'toc', 'bin', 'img',
                      'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['mednafen_psx_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_psx_libretro')
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
        return ['playstation']

 # Tries to identify files by any magic necessary

    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformPs2(PlatformCommon):
    def run(self):
        extensions = ['exe', 'psexe', 'cue', 'toc', 'bin', 'img',
                      'iso', 'chd', 'pbp', 'ccd', 'ecm', 'cbn', 'mdf', 'mds', 'psf', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['pcsx2_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('pcsx2_libretro')
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
        return ['playstation2']

 # Tries to identify files by any magic necessary

    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files


class PlatformPsp(PlatformCommon):
    def run(self):
        extensions = ['elf', 'iso', 'cso', 'prx', 'pbp']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['ppsspp_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('ppsspp_libretro')
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
        return ['playstationportable']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
