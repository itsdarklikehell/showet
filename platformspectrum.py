from platformcommon import PlatformCommon
import os

fullscreen = ['false']


class PlatformSpectrum(PlatformCommon):
    def run(self):
        extensions = ['tzx', 'tap', 'z80', 'rzx', 'scl', 'trd', 'dsk', 'zip']
        print("Supported extensions:", extensions)

        tzxs = self.find_files_with_extension('tzx')
        taps = self.find_files_with_extension('tap')
        z80s = self.find_files_with_extension('z80')
        rzxs = self.find_files_with_extension('rzx')
        scls = self.find_files_with_extension('scl')
        trds = self.find_files_with_extension('trd')
        dsks = self.find_files_with_extension('dsk')
        zips = self.find_files_with_extension('zip')

        if len(tzxs) == 0:
            tzxs = self.find_tzx_files()
        if len(taps) == 0:
            taps = self.find_tap_files()
        if len(z80s) == 0:
            z80s = self.find_z80_files()
        if len(rzxs) == 0:
            rzxs = self.find_rzx_files()
        if len(scls) == 0:
            scls = self.find_scl_files()
        if len(trds) == 0:
            trds = self.find_trd_files()
        if len(dsks) == 0:
            dsks = self.find_dsk_files()
        if len(zips) == 0:
            zips = self.find_zip_files()
        if len(trds) == 0 and len(taps) == 0 and len(tzxs) == 0 and len(z80s) == 0 and len(rzxs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        if emulator == 'retroarch':
            emulator.append('-L')
            emulator.append('fuse_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplitrd.vfl"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in tzxs:
                f.write(disk + "\n")
            for disk in taps:
                f.write(disk + "\n")
            for disk in z80s:
                f.write(disk + "\n")
            for disk in rzxs:
                f.write(disk + "\n")
            for disk in scls:
                f.write(disk + "\n")
            for disk in trds:
                f.write(disk + "\n")
            for disk in dsks:
                f.write(disk + "\n")
            for disk in zips:
                f.write(disk + "\n")

        if len(tzxs) > 0:
            tzxs = self.sort_disks(tzxs)
            if emulator == 'retroarch':
                emulator = emulator + [tzxs[0]]

        if len(taps) > 0:
            taps = self.sort_disks(taps)
            if emulator == 'retroarch':
                emulator = emulator + [taps[0]]

        if len(z80s) > 0:
            z80s = self.sort_disks(z80s)
            if emulator == 'retroarch':
                emulator = emulator + [z80s[0]]

        if len(rzxs) > 0:
            rzxs = self.sort_disks(rzxs)
            if emulator == 'retroarch':
                emulator = emulator + [rzxs[0]]

        if len(scls) > 0:
            scls = self.sort_disks(scls)
            if emulator == 'retroarch':
                emulator = emulator + [scls[0]]

        if len(trds) > 0:
            trds = self.sort_disks(trds)
            if emulator == 'retroarch':
                emulator = emulator + [trds[0]]

        if len(dsks) > 0:
            dsks = self.sort_disks(dsks)
            if emulator == 'retroarch':
                emulator = emulator + [dsks[0]]

        if len(zips) > 0:
            zips = self.sort_disks(zips)
            if emulator == 'retroarch':
                emulator = emulator + [zips[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['zxspectrum', 'spectrum']

# Tries to identify files by any magic necessary
    def find_tap_files(self):
        tap_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                tap_files.append(file)
        return tap_files

    def find_tzx_files(self):
        tzx_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                tzx_files.append(file)
        return tzx_files

    def find_z80_files(self):
        z80_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                z80_files.append(file)
        return z80_files

    def find_rzx_files(self):
        rzx_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                rzx_files.append(file)
        return rzx_files

    def find_scl_files(self):
        scl_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                scl_files.append(file)
        return scl_files

    def find_trd_files(self):
        trd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                trd_files.append(file)
        return trd_files

    def find_dsk_files(self):
        dsk_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dsk_files.append(file)
        return dsk_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zip_files.append(file)
        return zip_files
