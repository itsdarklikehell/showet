import os
from platformcommon import PlatformCommon

emulators = ['retroarch']
cores = ['retro8_libretro']
fullscreens = ['false']


class PlatformPico8(PlatformCommon):
    emulator = ['retroarch']
    core = ['retro8_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['p8', 'png']
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['retro8_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('retro8_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + emulator[0])
        print("\tUsing core: " + core[0])
        print("\tUsing fullscreen: " + fullscreen[0])

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
        return ['pico8']

 # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.diz'):
                ext_files.append(file)
                print("\tFound file: " + file)
        return ext_files
