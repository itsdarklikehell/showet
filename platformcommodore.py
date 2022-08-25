from platformcommon import PlatformCommon
import os

emulator = ['retroarch']
fullscreen = ['false']


class PlatformCommodore(PlatformCommon):
    def run(self):
        extensions = ['d64', 'd71', 'd80', 'd81', 'd82',
                      'g64', 'g41', 't64', 'tap', 'prg',
                      'p00', 'crt', 'bin', 'zip', 'gz',
                      'd6z', 'd7z', 'd8z', 'g4z', 'g6z',
                      'x6z', 'cmd', 'm3u', 'vfl', 'vsf',
                      'nib', 'nbz', 'd2m', 'd4m']
        print("Supported extensions:", extensions)

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
        bins = self.find_files_with_extension('bin')
        zips = self.find_files_with_extension('zip')
        gzs = self.find_files_with_extension('gz')
        d6zs = self.find_files_with_extension('d6z')
        d7zs = self.find_files_with_extension('d7z')
        d8zs = self.find_files_with_extension('d8z')
        g4zs = self.find_files_with_extension('g4z')
        g6zs = self.find_files_with_extension('g6z')
        x6zs = self.find_files_with_extension('x6z')
        cmds = self.find_files_with_extension('cmd')
        m3us = self.find_files_with_extension('m3u')
        vfls = self.find_files_with_extension('vfl')
        vsfs = self.find_files_with_extension('vsf')
        nibs = self.find_files_with_extension('nib')
        nbzs = self.find_files_with_extension('nbz')
        d2ms = self.find_files_with_extension('d2m')
        d4ms = self.find_files_with_extension('d4m')
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
        if len(t64s) == 0:
            t64s = self.find_t64_files()
        if len(taps) == 0:
            taps = self.find_tap_files()
        if len(prgs) == 0:
            prgs = self.find_prg_files()
        if len(p00s) == 0:
            p00s = self.find_p00_files()
        if len(crts) == 0:
            crts = self.find_crt_files()
        if len(bins) == 0:
            bins = self.find_bin_files()
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

        if len(d64s) == 0 and len(d71s) == 0 and len(d80s) == 0 and len(d81s) == 0 and len(d82s) == 0 and len(g64s) == 0 and len(g41s) == 0 and len(x64s) == 0 and len(t64s) == 0 and len(taps) == 0 and len(prgs) == 0 and len(p00s) == 0 and len(crts) == 0 and len(bins) == 0 and len(zips) == 0 and len(gzs) == 0 and len(d6zs) == 0 and len(d7zs) == 0 and len(d8zs) == 0 and len(g4zs) == 0 and len(g6zs) == 0 and len(x6zs) == 0 and len(cmds) == 0 and len(m3us) == 0 and len(vfls) == 0 and len(vsfs) == 0 and len(nibs) == 0 and len(nbzs) == 0 and len(d2ms) == 0 and len(d4ms) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('vice_x64_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

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
            for disk in x64s:
                f.write(disk + "\n")
            for disk in t64s:
                f.write(disk + "\n")
            for disk in taps:
                f.write(disk + "\n")
            for disk in prgs:
                f.write(disk + "\n")
            for disk in p00s:
                f.write(disk + "\n")
            for disk in crts:
                f.write(disk + "\n")
            for disk in bins:
                f.write(disk + "\n")
            for disk in zips:
                f.write(disk + "\n")
            for disk in gzs:
                f.write(disk + "\n")
            for disk in d6zs:
                f.write(disk + "\n")
            for disk in d7zs:
                f.write(disk + "\n")
            for disk in d8zs:
                f.write(disk + "\n")
            for disk in g4zs:
                f.write(disk + "\n")
            for disk in g6zs:
                f.write(disk + "\n")
            for disk in x6zs:
                f.write(disk + "\n")

        if len(d64s) > 0:
            d64s = self.sort_disks(d64s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [d64s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d64s[0]]

        if len(d71s) > 0:
            d71s = self.sort_disks(d71s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [d71s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d71s[0]]

        if len(d80s) > 0:
            d80s = self.sort_disks(d80s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [d80s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d80s[0]]

        if len(d81s) > 0:
            d81s = self.sort_disks(d81s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [d81s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d81s[0]]

        if len(d82s) > 0:
            d82s = self.sort_disks(d82s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [d82s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d82s[0]]

        if len(g64s) > 0:
            g64s = self.sort_disks(g64s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [g64s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g64s[0]]

        if len(g41s) > 0:
            g41s = self.sort_disks(g41s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [g41s[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g41s[0]]

        if len(x64s) > 0:
            x64s = self.sort_disks(x64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, x64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [x64s[0]]

        if len(t64s) > 0:
            t64s = self.sort_disks(t64s)
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, t64s[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [t64s[0]]

        if len(taps) > 0:
            taps = self.sort_disks(taps)
            if emulator[0] == 'retroarch':
                emulator = emulator + [taps[0]]
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, taps[0]]

        if len(prgs) > 0:
            prgs = self.sort_disks(prgs)
            if emulator[0] == 'retroarch':
                emulator.append(prgs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, prgs[0]]

        if len(p00s) > 0:
            p00s = self.sort_disks(p00s)
            if emulator[0] == 'retroarch':
                emulator.append(p00s[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, p00s[0]]

        if len(crts) > 0:
            crts = self.sort_disks(crts)
            if emulator[0] == 'retroarch':
                emulator.append(crts[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, crts[0]]

        if len(bins) > 0:
            bins = self.sort_disks(bins)
            if emulator[0] == 'retroarch':
                emulator.append(bins[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, bins[0]]

        if len(zips) > 0:
            zips = self.sort_disks(zips)
            if emulator[0] == 'retroarch':
                emulator.append(zips[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, zips[0]]

        if len(gzs) > 0:
            gzs = self.sort_disks(gzs)
            if emulator[0] == 'retroarch':
                emulator.append(gzs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, gzs[0]]

        if len(d6zs) > 0:
            d6zs = self.sort_disks(d6zs)
            if emulator[0] == 'retroarch':
                emulator.append(d6zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d6zs[0]]

        if len(d7zs) > 0:
            d7zs = self.sort_disks(d7zs)
            if emulator[0] == 'retroarch':
                emulator.append(d7zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d7zs[0]]

        if len(d8zs) > 0:
            d8zs = self.sort_disks(d8zs)
            if emulator[0] == 'retroarch':
                emulator.append(d8zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d8zs[0]]

        if len(g4zs) > 0:
            g4zs = self.sort_disks(g4zs)
            if emulator[0] == 'retroarch':
                emulator.append(g4zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g4zs[0]]

        if len(g6zs) > 0:
            g6zs = self.sort_disks(g6zs)
            if emulator[0] == 'retroarch':
                emulator.append(g6zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, g6zs[0]]

        if len(x6zs) > 0:
            x6zs = self.sort_disks(x6zs)
            if emulator[0] == 'retroarch':
                emulator.append(x6zs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, x6zs[0]]

        if len(m3us) > 0:
            m3us = self.sort_disks(m3us)
            if emulator[0] == 'retroarch':
                emulator.append(m3us[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, m3us[0]]

        if len(vfls) > 0:
            vfls = self.sort_disks(vfls)
            if emulator[0] == 'retroarch':
                emulator.append(vfls[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, vfls[0]]

        if len(vsfs) > 0:
            vsfs = self.sort_disks(vsfs)
            if emulator[0] == 'retroarch':
                emulator.append(vsfs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, vsfs[0]]

        if len(nibs) > 0:
            nibs = self.sort_disks(nibs)
            if emulator[0] == 'retroarch':
                emulator.append(nibs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, nibs[0]]

        if len(nbzs) > 0:
            nbzs = self.sort_disks(nbzs)
            if emulator[0] == 'retroarch':
                emulator.append(nbzs[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, nbzs[0]]

        if len(d2ms) > 0:
            d2ms = self.sort_disks(d2ms)
            if emulator[0] == 'retroarch':
                emulator.append(d2ms[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d2ms[0]]

        if len(d4ms) > 0:
            d4ms = self.sort_disks(d4ms)
            if emulator[0] == 'retroarch':
                emulator.append(d4ms[0])
            if emulator[0] == 'x64':
                emulator = emulator + ['-flipname', flipfile, d4ms[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['commodore64']

# Tries to identify files by any magic necessary
    def find_d64_files(self):
        d64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d64_files.append(file)
        return d64_files

    def find_d71_files(self):
        d71_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d71_files.append(file)
        return d71_files

    def find_d80_files(self):
        d80_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d80_files.append(file)
        return d80_files

    def find_d81_files(self):
        d81_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d81_files.append(file)
        return d81_files

    def find_d82_files(self):
        d82_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d82_files.append(file)
        return d82_files

    def find_g64_files(self):
        g64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                g64_files.append(file)
        return g64_files

    def find_g41_files(self):
        g41_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                g41_files.append(file)
        return g41_files

    def find_x64_files(self):
        x64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                x64_files.append(file)
        return x64_files

    def find_tap_files(self):
        tap_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                tap_files.append(file)
        return tap_files

    def find_t64_files(self):
        t64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                t64_files.append(file)
        return t64_files

    def find_prg_files(self):
        prg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                prg_files.append(file)
        return prg_files

    def find_p00_files(self):
        p00_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                p00_files.append(file)
        return p00_files

    def find_crt_files(self):
        crt_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                crt_files.append(file)
        return crt_files

    def find_bin_files(self):
        bin_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bin_files.append(file)
        return bin_files

    def find_cmd_files(self):
        cmd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                cmd_files.append(file)
        return cmd_files

    def find_m3u_files(self):
        m3u_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                m3u_files.append(file)
        return m3u_files

    def find_vfl_files(self):
        vfl_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                vfl_files.append(file)
        return vfl_files

    def find_vsf_files(self):
        vsf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                vsf_files.append(file)
        return vsf_files

    def find_nib_files(self):
        nib_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nib_files.append(file)
        return nib_files

    def find_nbz_files(self):
        nbz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nbz_files.append(file)
        return nbz_files

    def find_d2m_files(self):
        d2m_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d2m_files.append(file)
        return d2m_files

    def find_d4m_files(self):
        d4m_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d4m_files.append(file)
        return d4m_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zip_files.append(file)
        return zip_files

    def find_gz_files(self):
        gz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gz_files.append(file)
        return gz_files

    def find_d6z_files(self):
        d6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d6z_files.append(file)
        return d6z_files

    def find_d7z_files(self):
        d7z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d7z_files.append(file)
        return d7z_files

    def find_d8z_files(self):
        d8z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                d8z_files.append(file)
        return d8z_files

    def find_g4z_files(self):
        g4z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                g4z_files.append(file)
        return g4z_files

    def find_g6z_files(self):
        g6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                g6z_files.append(file)
        return g6z_files

    def find_x6z_files(self):
        x6z_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                x6z_files.append(file)
        return x6z_files
