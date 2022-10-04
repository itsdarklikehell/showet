import os
import os.path
from platformcommon import PlatformCommon

class Platform_Pcengine(PlatformCommon):
    emulators = ['retroarch']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro',
             'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mednafen_supergrafx_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_supergrafx_libretro')
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
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Supergrafx(PlatformCommon):
    emulators = ['retroarch']
    cores = ['mednafen_supergrafx_libretro', 'mednafen_pce_fast_libretro',
             'fbneo_pce_libretro', 'fbneo_sgx_libretro', 'fbneo_tg_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mednafen_supergrafx_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['mednafen_supergrafx_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_supergrafx_libretro')
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
        return ['necturbografxpcengine']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Pc8000(PlatformCommon):
    emulators = ['retroarch']
    cores = ['quasi88_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['quasi88_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['quasi88_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('quasi88_libretro')
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
        return ['pc8000', 'pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Pc8800(PlatformCommon):
    emulators = ['retroarch']
    cores = ['quasi88_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['quasi88_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['quasi88_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('quasi88_libretro')
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
        return ['pc8800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Pc98(PlatformCommon):
    emulators = ['retroarch']
    cores = ['nekop2_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['nekop2_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['nekop2_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('nekop2_libretro')
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
        return ['pc-98']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Pcfx(PlatformCommon):
    emulators = ['retroarch']
    cores = ['mednafen_pcfx_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mednafen_pcfx_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'pce', 'sgx', 'cue', 'ccd', 'chd']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['mednafen_pcfx_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_pcfx_libretro')
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
        return ['pcfx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.nfo') and not file.endswith('.DIZ') and not file.endswith('.DOC') and not file.endswith('.NOW') and not file.endswith('.JPG') and not file.endswith('.ANS') and not file.endswith('.DAT') and not file.endswith('.ION'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
