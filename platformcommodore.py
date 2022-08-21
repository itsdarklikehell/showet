from platformcommon import PlatformCommon
import os


class PlatformCommodore(PlatformCommon):
    def run(self):
        d64s = self.find_files_with_extension('d64')
        d71s = self.find_files_with_extension('d71')
        d80s = self.find_files_with_extension('d80')
        d81s = self.find_files_with_extension('d81')
        d82s = self.find_files_with_extension('d82')
        g64s = self.find_files_with_extension('g64')
        t64s = self.find_files_with_extension('t64')
        prgs = self.find_files_with_extension('prg')

        if len(d64s) == 0:
            d64s = self.find_d64_files()

        if len(d71s) == 0:
            d71s = self.find_d71_files()

        if len(d80s) == 0:
            d80s = self.find_d80_files()

        if len(d81s) == 0:
            d81s = self.find_d81_files()

        if len(d82s) == 0:
            d82s = self.find_d82_files()

        if len(g64s) == 0:
            g64s = self.find_g64_files()

        if len(t64s) == 0:
            g64s = self.find_t64_files()

        if len(prgs) == 0:
            prgs = self.find_prg_files()

        if len(d64s) == 0 and len(t64s) == 0 and len(prgs) == 0:
            print("Didn't find any executable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('vice_x64_libretro')
        # emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in d64s:
                f.write(disk + "\n")
            for disk in d71s:
                f.write(disk + "\n")
            for disk in d80s:
                f.write(disk + "\n")
            for disk in d81s:
                f.write(disk + "\n")
            for disk in d82s:
                f.write(disk + "\n")
            for disk in g64s:
                f.write(disk + "\n")
            for disk in t64s:
                f.write(disk + "\n")
            for disk in prgs:
                f.write(disk + "\n")

        if len(d64s) > 0:
            d64s = self.sort_disks(d64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [d64s[0]]

        if len(t64s) > 0:
            t64s = self.sort_disks(t64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, t64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [t64s[0]]

        if len(prgs) > 0:
            emulator.append(prgs[0])

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore64']

# # Tries to identify files by any magic necessary
#     def find_files(self):
#         files = []
#         for file in self.prod_files:
#             size = os.path.getsize(file)
#             if size == 174848:  # All d64:s seem to be this size..
#                 files.append(file)
#         return files

# Tries to identify d64 files by any magic necessary
    def find_d64_files(self):
        d64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d64:s seem to be this size..
                d64_files.append(file)
        return d64_files

# Tries to identify d71 files by any magic necessary
    def find_d71_files(self):
        d71_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All 71:s seem to be this size..
                d71_files.append(file)
        return d71_files

# Tries to identify d80 files by any magic necessary
    def find_d80_files(self):
        d80_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d80:s seem to be this size..
                d80_files.append(file)
        return d80_files

# Tries to identify d81 files by any magic necessary
    def find_d81_files(self):
        d81_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d81:s seem to be this size..
                d81_files.append(file)
        return d81_files

# Tries to identify d82 files by any magic necessary
    def find_d82_files(self):
        d82_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d82:s seem to be this size..
                d82_files.append(file)
        return d82_files

# Tries to identify g64 files by any magic necessary
    def find_g64_files(self):
        g64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All g64:s seem to be this size..
                g64_files.append(file)
        return g64_files

# Tries to identify t64 files by any magic necessary
    def find_t64_files(self):
        t64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All t64:s seem to be this size..
                t64_files.append(file)
        return t64_files

# Tries to identify prg files by any magic necessary
    def find_prg_files(self):
        prg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All prg:s seem to be this size..
                prg_files.append(file)
        return prg_files
