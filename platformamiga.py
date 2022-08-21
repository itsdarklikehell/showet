from platformcommon import PlatformCommon
import os


class PlatformAmiga(PlatformCommon):
    def run(self):
        adfs = self.find_files_with_extension('adf')
        adzs = self.find_files_with_extension('adz')
        dmss = self.find_files_with_extension('dms')
        exes = self.find_files_with_extension('exe')
        if len(exes) == 0:
            exes = self.find_magic_cookies()

        if len(adfs) == 0 and len(adzs) == 0 and len(dmss) == 0 and len(exes) == 0:
            print("Didn't find any dms, adf or executable files.")
            exit(-1)

        #emulator = ['fs-uae', '--fullscreen', '--keep_aspect']
        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('puae_libretro')
        # emulator.append('--fullscreen')

        drives = []
        # Support only one for now..
        if len(dmss) > 0:
            drives = self.sort_disks(dmss)
        elif len(adfs) > 0:
            drives = self.sort_disks(adfs)
        elif len(adzs) > 0:
            drives = self.sort_disks(adzs)
        elif len(exes) > 0:
            if emulator[0] == 'fs-uae':
                emulator.append('--hard_drive_0=.')
            # if emulator[0] == 'retroarch':
                # emulator.append('--hard_drive_0=.')

            if not os.path.exists(self.datadir + "/s"):
                os.makedirs(self.datadir + "/s")
# TODO: when find_files_with_extension works with paths relative to datadir, we can simplify this
                with open(self.datadir + "/s/startup-sequence", 'w') as f:
                    exename = exes[0].split('/')
                    exename = exename[len(exename)-1]
                    f.write(exename + "\n")
                    f.close()
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
        return ['amigaocsecs', 'amigaaga']

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
