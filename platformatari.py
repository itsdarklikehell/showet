from platformcommon import PlatformCommon
import os


class PlatformAtarist(PlatformCommon):
    def run(self):
        extensions = ['st', 'msa', 'stx', 'ipf', 'm3u', 'vsf', 'zip']
        print("Supported extensions:", extensions)

        sts = self.find_files_with_extension('st')
        msas = self.find_files_with_extension('msa')
        stxs = self.find_files_with_extension('stx')
        ipfs = self.find_files_with_extension('ipf')
        m3us = self.find_files_with_extension('m3u')
        vsfs = self.find_files_with_extension('vsf')
        zips = self.find_files_with_extension('zip')

        if len(sts) == 0:
            sts = self.find_st_files()
        if len(msas) == 0:
            msas = self.find_msa_files()
        if len(stxs) == 0:
            stxs = self.find_stx_files()
        if len(ipfs) == 0:
            ipfs = self.find_ipf_files()
        if len(m3us) == 0:
            m3us = self.find_m3u_files()
        if len(vsfs) == 0:
            vsfs = self.find_vsf_files()
        if len(zips) == 0:
            vsfs = self.find_zip_files()
        if len(sts) == 0 and len(msas) == 0 and len(stxs) == 0 and len(ipfs) == 0 and len(m3us) == 0 and len(vsfs) == 0 and len(zips) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('hatari_libretro')
        # emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in sts:
                f.write(disk + "\n")
            for disk in msas:
                f.write(disk + "\n")
            for disk in stxs:
                f.write(disk + "\n")
            for disk in ipfs:
                f.write(disk + "\n")
            for disk in m3us:
                f.write(disk + "\n")
            for disk in vsfs:
                f.write(disk + "\n")
            for disk in zips:
                f.write(disk + "\n")

        if len(sts) > 0:
            sts = self.sort_disks(sts)
            if emulator[0] == 'retroarch':
                emulator = emulator + [sts[0]]

        if len(msas) > 0:
            msas = self.sort_disks(msas)
            if emulator[0] == 'retroarch':
                emulator = emulator + [msas[0]]

        if len(stxs) > 0:
            stxs = self.sort_disks(stxs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [stxs[0]]

        if len(ipfs) > 0:
            ipfs = self.sort_disks(ipfs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [ipfs[0]]

        if len(m3us) > 0:
            m3us = self.sort_disks(m3us)
            if emulator[0] == 'retroarch':
                emulator = emulator + [m3us[0]]

        if len(vsfs) > 0:
            vsfs = self.sort_disks(vsfs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [vsfs[0]]

        if len(zips) > 0:
            zips = self.sort_disks(zips)
            if emulator[0] == 'retroarch':
                emulator = emulator + [zips[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarist', 'atariste']

# Tries to identify files by any magic necessary
    def find_st_files(self):
        st_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                st_files.append(file)
        return st_files

    def find_msa_files(self):
        msa_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                msa_files.append(file)
        return msa_files

    def find_stx_files(self):
        stx_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                stx_files.append(file)
        return stx_files

    def find_ipf_files(self):
        ipf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ipf_files.append(file)
        return ipf_files

    def find_m3u_files(self):
        m3u_files = []
        for file in self.prod_files:
            m3u_files.append(file)
        return m3u_files

    def find_vsf_files(self):
        vsf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                vsf_files.append(file)
        return vsf_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zip_files.append(file)
        return zip_files


class PlatformAtarixlxe(PlatformCommon):
    def run(self):
        extensions = ['xfd', 'atr', 'xfdx', 'cdm',
                      'cas', 'bin', 'a52', 'xex', 'zip']
        print("Supported extensions:", extensions)

        xfds = self.find_files_with_extension('xfd')
        atrs = self.find_files_with_extension('atr')
        atxs = self.find_files_with_extension('atx')
        cdms = self.find_files_with_extension('cdm')
        cass = self.find_files_with_extension('cas')
        bins = self.find_files_with_extension('bin')
        a52s = self.find_files_with_extension('a52')
        xexs = self.find_files_with_extension('xex')
        zips = self.find_files_with_extension('zip')

        if len(xfds) == 0:
            xfds = self.find_xfd_files()
        if len(atrs) == 0:
            atrs = self.find_atr_files()
        if len(atxs) == 0:
            atxs = self.find_xfdx_files()
        if len(cdms) == 0:
            cdms = self.find_cdm_files()
        if len(cass) == 0:
            cass = self.find_cas_files()
        if len(bins) == 0:
            bins = self.find_bin_files()
        if len(a52s) == 0:
            a52s = self.find_a52_files()
        if len(xexs) == 0:
            xexs = self.find_xexs_files()
        if len(zips) == 0:
            zips = self.find_zip_files()
        if len(xfds) == 0 and len(atrs) == 0 and len(atx) == 0 and len(cdms) == 0 and len(cass) == 0 and len(bins) == 0 and len(zips) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('hatari_libretro')
        # emulator.append('--fullscreen')

        flcdmile = self.datadir + "/fliplixfd.vfl"
        with open(flcdmile, "w") as f:
            f.write("UNIT 8\n")
            for disk in xfds:
                f.write(disk + "\n")
            for disk in atrs:
                f.write(disk + "\n")
            for disk in atx:
                f.write(disk + "\n")
            for disk in cdms:
                f.write(disk + "\n")
            for disk in cass:
                f.write(disk + "\n")
            for disk in bins:
                f.write(disk + "\n")
            for disk in a52s:
                f.write(disk + "\n")
            for disk in xexs:
                f.write(disk + "\n")
            for disk in zips:
                f.write(disk + "\n")

        if len(xfds) > 0:
            xfds = self.sort_disks(xfds)
            if emulator[0] == 'retroarch':
                emulator = emulator + [xfds[0]]

        if len(atrs) > 0:
            atrs = self.sort_disks(atrs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [atrs[0]]

        if len(atx) > 0:
            atx = self.sort_disks(atx)
            if emulator[0] == 'retroarch':
                emulator = emulator + [atx[0]]

        if len(cdms) > 0:
            cdms = self.sort_disks(cdms)
            if emulator[0] == 'retroarch':
                emulator = emulator + [cdms[0]]

        if len(cass) > 0:
            cass = self.sort_disks(cass)
            if emulator[0] == 'retroarch':
                emulator = emulator + [cass[0]]

        if len(bins) > 0:
            bins = self.sort_disks(bins)
            if emulator[0] == 'retroarch':
                emulator = emulator + [bins[0]]

        if len(a52s) > 0:
            a52s = self.sort_disks(a52s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [a52s[0]]

        if len(xexs) > 0:
            xexs = self.sort_disks(xexs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [xexs[0]]

        if len(zips) > 0:
            zips = self.sort_disks(zips)
            if emulator[0] == 'retroarch':
                emulator = emulator + [zips[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

# Tries to identify files by any magic necessary
    def find_xfd_files(self):
        xfd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                xfd_files.append(file)
        return xfd_files

    def find_atr_files(self):
        atr_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                atr_files.append(file)
        return atr_files

    def find_xfdx_files(self):
        xfdx_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                xfdx_files.append(file)
        return xfdx_files

    def find_cdm_files(self):
        cdm_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                cdm_files.append(file)
        return cdm_files

    def find_cas_files(self):
        cas_files = []
        for file in self.prod_files:
            cas_files.append(file)
        return cas_files

    def find_bin_files(self):
        bin_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bin_files.append(file)
        return bin_files

    def find_a52_files(self):
        a52_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                a52_files.append(file)
        return a52_files

    def find_xex_files(self):
        xex_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                xex_files.append(file)
        return xex_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zip_files.append(file)
        return zip_files
