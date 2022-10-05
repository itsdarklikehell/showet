import os
import os.path
from platformcommon import PlatformCommon

class Platform_Apple(PlatformCommon):
    emulators = ['retroarch', 'linapple', 'basilisk']
    cores = ['minivmac_libretro']
    fullscreens = ['false']

    # emulator = ['retroarch']
    # core = ['minivmac_libretro']
    # fullscreen = ['false']

    def run(self):
        extensions = ['dsk', 'img', 'zip', 'hvf', 'cmd']
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary    
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['minivmac_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('minivmac_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        if emulator[0] == 'linapple':
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

        # Sort the files.
        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['appleii', 'appleiigs']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if not file.endswith('.json') or file.endswith('.txt') or file.endswith('.diz') or file.endswith('.png'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
