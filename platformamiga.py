from platformcommon import PlatformCommon
import os

# emulator = ['fs-uae']
emulator = ['retroarch']
fullscreen = ['false']


class PlatformAmiga(PlatformCommon):
    def run(self):
        extensions = ['zip', 'm3u', 'adf', 'adz', 'dms', 'fdi', 'ipf', 'hdf', 'hdz', 'lha', 'tga', 'slave', 'info',
                      'cue', 'ccd', 'nrg', 'mds', 'iso', 'chd', 'uae', '7z', 'rp9', 'exe', 'run']

        ext = []
        for ext in extensions:
            print("looking for files ending with: " + ext)
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('puae_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')
        if emulator[0] == 'fs-uae':
            if fullscreen == 'true':
                emulator.append('--fullscreen')
                emulator.append('--keep_aspect')
        drives = []
        # Support only one for now..
        if len(files) > 0:
            if emulator[0] == 'fs-uae':
                emulator.append('--hard_drive_0=.')
            if emulator[0] == 'retroarch':
                # emulator.append('--hard_drive_0=.')
                emulator = emulator + [files[0]]

            if not os.path.exists(self.datadir + "/s"):
                os.makedirs(self.datadir + "/s")
        #         # TODO: when find_files_with_extension works with paths relative to datadir, we can simplify this
                with open(self.datadir + "/s/startup-sequence", 'w') as f:
                    exename = files[0].split('/')
                    exename = exename[len(exename)-1]
                    f.write(exename + "\n")
                    f.close()
        if len(files) > 0:
            drives = self.sort_disks(files)
            emulator = emulator + [files[0]]

        if emulator[0] == 'fs-uae':
            amiga_model = 'A1200'
            if self.prod_platform == 'amigaocsecs':
                amiga_model = 'A500'

            if self.prod_platform == 'amigaaga':
                emulator.append('--fast_memory=8192')
    # --chip_memory=2048
            if len(drives) > 0:
                emulator.append('--floppy_drive_0=' + drives[0])
            if len(drives) > 1:
                emulator.append('--floppy_drive_1=' + drives[1])
            if len(drives) > 2:
                emulator.append('--floppy_drive_2=' + drives[2])
            if len(drives) > 3:
                emulator.append('--floppy_drive_3=' + drives[3])

            emulator.append('--model=' + amiga_model)
        if emulator[0] == 'retroarch':
            amiga_model = 'A1200'

            if self.prod_platform == 'amigaocsecs':
                amiga_model = 'A500'

    # --chip_memory=2048

            if len(drives) > 0:
                emulator.append('drives[0]')
            if len(drives) > 1:
                emulator.append('drives[1]')
            if len(drives) > 2:
                emulator.append('drives[2]')
            if len(drives) > 3:
                emulator.append('drives[3]')

        self.run_process(emulator)

    def supported_platforms(self):
        return ['amigaocsecs', 'amigaaga', 'amigappcrtg']

# Search demo files for amiga magic cookie (executable file)
    def find_magic_cookies(self):
        cookie_files = []
        for file in self.prod_files:
            with open(file, "rb") as fin:
                header = fin.read(4)
                if len(header) == 4:
                    # Signature for Amiga magic cookie
                    if header[0] == 0 and header[1] == 0 and header[2] == 3 and header[3] == 243:
                        cookie_files.append(file)
        return cookie_files


# Tries to identify files by any magic necessary

    def find_ext_files(self):
        exclusions = ['.json', '.DIZ']
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith(exclusions):
                    ext_files.append(file)
                    print("Found file: " + file)
        return ext_files
