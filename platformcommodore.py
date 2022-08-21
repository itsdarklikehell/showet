from platformcommon import PlatformCommon
import os


class PlatformCommodore(PlatformCommon):
    def run(self):
        # executables:
        d64s = self.find_files_with_extension('d64')
        d71s = self.find_files_with_extension('d71')
        d80s = self.find_files_with_extension('d80')
        d81s = self.find_files_with_extension('d81')
        d82s = self.find_files_with_extension('d82')
        g64s = self.find_files_with_extension('g64')
        g41s = self.find_files_with_extension('g41')
        x64s = self.find_files_with_extension('x64')
        t64s = self.find_files_with_extension('t64')
        taps = self.find_files_with_extension('tap')
        prgs = self.find_files_with_extension('prg')
        p00s = self.find_files_with_extension('p00')
        crts = self.find_files_with_extension('crt')
        cmds = self.find_files_with_extension('cmd')
        m3us = self.find_files_with_extension('m3u')
        vfls = self.find_files_with_extension('vfl')
        vsfs = self.find_files_with_extension('vsf')
        nibs = self.find_files_with_extension('nib')
        nbzs = self.find_files_with_extension('nbz')
        d2ms = self.find_files_with_extension('d2m')
        d4ms = self.find_files_with_extension('d4m')
# compressed file types:
        zips = self.find_files_with_extension('zip')
        gzs = self.find_files_with_extension('gz')
        d6zs = self.find_files_with_extension('d6z')
        d7zs = self.find_files_with_extension('d7z')
        d8zs = self.find_files_with_extension('d8z')
        g4zs = self.find_files_with_extension('g4z')
        g6zs = self.find_files_with_extension('g6z')
        x6zs = self.find_files_with_extension('x6z')

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

        if len(g41s) == 0:
            g41s = self.find_g41_files()

        if len(x64s) == 0:
            x64s = self.find_x64_files()

        if len(taps) == 0:
            taps = self.find_tap_files()

        if len(t64s) == 0:
            t64s = self.find_t64_files()

        if len(prgs) == 0:
            prgs = self.find_prg_files()

        if len(p00s) == 0:
            p00s = self.find_p00_files()

        if len(crts) == 0:
            crts = self.find_crt_files()

        if len(cmds) == 0:
            cmds = self.find_cmd_files()

        if len(m3us) == 0:
            m3us = self.find_m3u_files()

        if len(vfls) == 0:
            vfls = self.find_vfl_files()

        if len(vsfs) == 0:
            vsfs = self.find_vsf_files()

        if len(nibs) == 0:
            nibs = self.find_nib_files()

        if len(nbzs) == 0:
            nbzs = self.find_nbz_files()

        if len(d2ms) == 0:
            d2ms = self.find_d2m_files()

        if len(d4ms) == 0:
            d4ms = self.find_d4m_files()

        if len(zips) == 0:
            zips = self.find_zip_files()

        if len(gzs) == 0:
            gzs = self.find_gz_files()

        if len(d6zs) == 0:
            d6zs = self.find_d6z_files()

        if len(d7zs) == 0:
            d7zs = self.find_d7z_files()

        if len(d8zs) == 0:
            d8zs = self.find_d8z_files()

        if len(g4zs) == 0:
            g4zs = self.find_g4z_files()

        if len(g6zs) == 0:
            g6zs = self.find_g6z_files()

        if len(x6zs) == 0:
            x6zs = self.find_x6z_files()

        if len(d64s) == 0 and len(d71s) == 0 and len(d80s) == 0 and len(d81s) == 0 and len(d82s) == 0 and len(g64s) == 0 and len(g41s) == 0 and len(x64s) == 0 and len(taps) == 0 and len(prgs) == 0 and len(p00s) == 0 and len(crts) == 0 and len(cmds) == 0 and len(m3us) == 0 and len(vfls) == 0 and len(vsfs) == 0 and len(nibs) == 0 and len(nbzs) == 0 and len(d2ms) == 0 and len(d4ms) == 0 and len(zips) == 0 and len(gzs) == 0 and len(d6zs) == 0 and len(d7zs) == 0 and len(d8zs) == 0 and len(g4zs) == 0 and len(g6zs) == 0 and len(x6zs) == 0:
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
            for disk in g41s:
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

        if len(d71s) > 0:
            d71s = self.sort_disks(d71s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d71s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [d71s[0]]

        if len(d80s) > 0:
            d80s = self.sort_disks(d80s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d80s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [d80s[0]]

        if len(d81s) > 0:
            d81s = self.sort_disks(d81s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d81s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [d81s[0]]

        if len(d82s) > 0:
            d82s = self.sort_disks(d82s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d82s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [d82s[0]]

        if len(g64s) > 0:
            g64s = self.sort_disks(g64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [g64s[0]]

        if len(g41s) > 0:
            g41s = self.sort_disks(g41s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g41s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [g41s[0]]

        if len(x64s) > 0:
            x64s = self.sort_disks(x64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, x64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [x64s[0]]

        if len(taps) > 0:
            taps = self.sort_disks(taps)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, taps[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [taps[0]]

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

# Tries to identify g41 files by any magic necessary
    def find_g41_files(self):
        g41_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All g41:s seem to be this size..
                g41_files.append(file)
        return g41_files

# Tries to identify x64 files by any magic necessary
    def find_x64_files(self):
        x64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All x64:s seem to be this size..
                x64_files.append(file)
        return x64_files

# Tries to identify tap files by any magic necessary
    def find_tap_files(self):
        tap_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All tap:s seem to be this size..
                tap_files.append(file)
        return tap_files

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

# Tries to identify p00 files by any magic necessary
    def find_p00_files(self):

        p00_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All p00:s seem to be this size..
                p00_files.append(file)
        return p00_files

# Tries to identify crt files by any magic necessary
    def find_crt_files(self):

        crt_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All crt:s seem to be this size..
                crt_files.append(file)
        return crt_files

# Tries to identify cmd files by any magic necessary
    def find_cmd_files(self):

        cmd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All cmd:s seem to be this size..
                cmd_files.append(file)
        return cmd_files

# Tries to identify m3u files by any magic necessary
    def find_m3u_files(self):

        m3u_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All m3u:s seem to be this size..
                m3u_files.append(file)
        return m3u_files

# Tries to identify vfl files by any magic necessary
    def find_vfl_files(self):

        vfl_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All vfl:s seem to be this size..
                vfl_files.append(file)
        return vfl_files

# Tries to identify vsf files by any magic necessary
    def find_vsf_files(self):

        vsf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All vsf:s seem to be this size..
                vsf_files.append(file)
        return vsf_files

# Tries to identify nib files by any magic necessary
    def find_nib_files(self):

        nib_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All nib:s seem to be this size..
                nib_files.append(file)
        return nib_files

# Tries to identify nbz files by any magic necessary
    def find_nbz_files(self):

        nbz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All nbz:s seem to be this size..
                nbz_files.append(file)
        return nbz_files

# Tries to identify d2m files by any magic necessary
    def find_d2m_files(self):

        d2m_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d2m:s seem to be this size..
                d2m_files.append(file)
        return d2m_files

# Tries to identify d4m files by any magic necessary
    def find_d4m_files(self):

        d4m_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d4m:s seem to be this size..
                d4m_files.append(file)
        return d4m_files

# Tries to identify zip files by any magic necessary
    def find_zip_files(self):

        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All zip:s seem to be this size..
                zip_files.append(file)
        return zip_files

# Tries to identify gz files by any magic necessary
    def find_gz_files(self):

        gz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All gz:s seem to be this size..
                gz_files.append(file)
        return gz_files

# Tries to identify d6z files by any magic necessary
    def find_d6z_files(self):
        d6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d6z:s seem to be this size..
                d6z_files.append(file)
        return d6z_files

# Tries to identify d7z files by any magic necessary
    def find_d7z_files(self):
        d7z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d7z:s seem to be this size..
                d7z_files.append(file)
        return d7z_files

# Tries to identify d8z files by any magic necessary
    def find_d8z_files(self):
        d8z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All d8z:s seem to be this size..
                d8z_files.append(file)
        return d8z_files

# Tries to identify g4z files by any magic necessary
    def find_g4z_files(self):
        g4z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All g4z:s seem to be this size..
                g4z_files.append(file)
        return g4z_files

# Tries to identify g6z files by any magic necessary
    def find_g6z_files(self):
        g6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All g6z:s seem to be this size..
                g6z_files.append(file)
        return g6z_files

# Tries to identify x6z files by any magic necessary
    def find_x6z_files(self):
        x6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:  # All x6z:s seem to be this size..
                x6z_files.append(file)
        return x6z_files
