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

        # flipfile = self.datadir + "/fliplist.vfl"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in sts:
        #         f.write(disk + "\n")
        #     for disk in msas:
        #         f.write(disk + "\n")
        #     for disk in stxs:
        #         f.write(disk + "\n")
        #     for disk in ipfs:
        #         f.write(disk + "\n")
        #     for disk in m3us:
        #         f.write(disk + "\n")
        #     for disk in vsfs:
        #         f.write(disk + "\n")
        #     for disk in zips:
        #         f.write(disk + "\n")

        if len(sts) > 0:
            sts = self.sort_disks(sts)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, sts[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [sts[0]]

        if len(msas) > 0:
            msas = self.sort_disks(msas)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, msas[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [msas[0]]

        if len(stxs) > 0:
            stxs = self.sort_disks(stxs)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, stxs[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [stxs[0]]

        if len(ipfs) > 0:
            ipfs = self.sort_disks(ipfs)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, ipfs[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [ipfs[0]]

        if len(m3us) > 0:
            m3us = self.sort_disks(m3us)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, m3us[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [m3us[0]]

        if len(vsfs) > 0:
            vsfs = self.sort_disks(vsfs)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, vsfs[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [vsfs[0]]

        if len(zips) > 0:
            zips = self.sort_disks(zips)
            # if emulator[0] == 'vsf':
            #     emulator = emulator + ['-flipname', flipfile, zips[0]]
            if emulator[0] == 'retroarch':
                emulator = emulator + [zips[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarist', 'atariste']

# Tries to identify files by any magic necessary
    def find_st_files(self):
        st_files = []
        for file in self.prod_files:
            st_files.append(file)
        return st_files

    def find_msa_files(self):
        msa_files = []
        for file in self.prod_files:
            msa_files.append(file)
        return msa_files

    def find_stx_files(self):
        stx_files = []
        for file in self.prod_files:
            stx_files.append(file)
        return stx_files

    def find_ipf_files(self):
        ipf_files = []
        for file in self.prod_files:
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
            vsf_files.append(file)
        return vsf_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            zip_files.append(file)
        return zip_files
