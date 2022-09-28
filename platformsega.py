import os
from platformcommon import PlatformCommon

class PlatformMastersystem(PlatformCommon):
    emulators = ['retroarch', 'osmose']
    fullscreens = ['false']
    cores = ['genesis_plus_gx_libretro', 'fbneo_sms_libretro', 'gearsystem_libretro', 'picodrive_libretro', 'smsplus_gx_libreto']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['genesis_plus_gx_libretro']
    def run(self):
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                      'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['genesis_plus_gx_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('genesis_plus_gx_libretro')
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
        return ['segamastersystem']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformGenesis(PlatformCommon):
    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['blastem_libretro']

    def run(self):
        extensions = ['zip', 'md', 'bin', 'smd', 'gen', '68k', 'sgd']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['blastem_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('blastem_libretro')
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
        return ['segagenesismegadrive']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformMegadrive(PlatformCommon):
    emulators = ['retroarch', 'dgen']
    fullscreens = ['false']
    cores = ['genesis_plus_gx_libretro', 'fbneo_md_libretro', 'picodrive_libretro']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['genesis_plus_gx_libretro']
    def run(self):
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso',
                      'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['genesis_plus_gx_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('genesis_plus_gx_libretro')
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
        return ['segagenesismegadrive']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformGamegear(PlatformCommon):
    emulators = ['retroarch', 'osmose']
    fullscreens = ['false']
    cores = ['gearsystem_libretro', 'genesis_plus_gx_libretro', 'fbneo_gg_libretro']
    
    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['gearsystem_libretro']
    def run(self):
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['gearsystem_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gearsystem_libretro')
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
        return ['segagamegear']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformFlycast(PlatformCommon):
    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['flycast_libretro']

    def run(self):
        extensions = ['zip', 'chd', 'cdi', 'iso', 'elf', 'bin',
                      'cue', 'gdi', 'lst', 'dat', '7z', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['flycast_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('flycast_libretro')
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
        return ['dreamcast']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformFlycastGLES2(PlatformCommon):
    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['flycast_gles2_libretro']

    def run(self):
        extensions = ['zip', 'chd', 'cdi', 'iso', 'elf', 'bin',
                      'cue', 'gdi', 'lst', 'dat', '7z', 'm3u']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['flycast_gles2_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('flycast_gles2_libretro')
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
        return ['dreamcast']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
class PlatformSaturn(PlatformCommon):
    emulators = ['retroarch', 'yabause', 'kronos']
    fullscreens = ['false']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    
    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['mednafen_saturn_libretro']
    def run(self):
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mednafen_saturn_libretro']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_saturn_libretro')
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
        return ['segasaturn']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz') and not file.endswith('.DIZ'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
