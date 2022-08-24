from cProfile import run
from platformcommon import PlatformCommon
import os

fullscreen = ['false']


class PlatformAmiga(PlatformCommon):
    def run(self):
        extensions = ['adf', 'adz', 'dms', 'fdi', 'ipf', 'hdf', 'hdz', 'lha', 'slave', 'info',
                      'cue', 'ccd', 'nrg', 'mds', 'iso', 'chd', 'uae', 'm3u', 'zip', '7z', 'rp9', 'exe', 'run']
        print("Supported extensions:", extensions)

        adfs = self.find_files_with_extension('adf')
        adzs = self.find_files_with_extension('adz')
        dmss = self.find_files_with_extension('dms')
        fdis = self.find_files_with_extension('fdi')
        ipfs = self.find_files_with_extension('ipf')
        hdfs = self.find_files_with_extension('hdf')
        hdzs = self.find_files_with_extension('hdz')
        lhas = self.find_files_with_extension('lha')
        slaves = self.find_files_with_extension('slave')
        infos = self.find_files_with_extension('info')
        cues = self.find_files_with_extension('cue')
        ccds = self.find_files_with_extension('ccd')
        nrgs = self.find_files_with_extension('nrg')
        mdss = self.find_files_with_extension('mds')
        isos = self.find_files_with_extension('iso')
        chds = self.find_files_with_extension('chd')
        uaes = self.find_files_with_extension('uae')
        m3us = self.find_files_with_extension('m3u')
        zips = self.find_files_with_extension('zip')
        zs = self.find_files_with_extension('7z')
        rp9s = self.find_files_with_extension('rp9')
        exes = self.find_files_with_extension('exe')
        runs = self.find_files_with_extension('run')

        if len(exes) == 0:
            exes = self.find_magic_cookies()
        if len(adfs) == 0:
            adfs = self.find_adf_files()
        if len(adzs) == 0:
            adzs = self.find_adz_files()
        if len(dmss) == 0:
            dmss = self.find_dms_files()
        if len(fdis) == 0:
            fdis = self.find_fdi_files()
        if len(ipfs) == 0:
            ipfs = self.find_ipf_files()
        if len(hdfs) == 0:
            hdfs = self.find_hdf_files()
        if len(hdzs) == 0:
            hdzs = self.find_hdz_files()
        if len(lhas) == 0:
            lhas = self.find_lha_files()
        if len(slaves) == 0:
            slaves = self.find_slave_files()
        if len(infos) == 0:
            infos = self.find_info_files()
        if len(cues) == 0:
            cues = self.find_cue_files()
        if len(ccds) == 0:
            ccds = self.find_ccd_files()
        if len(nrgs) == 0:
            nrgs = self.find_nrg_files()
        if len(mdss) == 0:
            mdss = self.find_mds_files()
        if len(isos) == 0:
            isos = self.find_iso_files()
        if len(chds) == 0:
            chds = self.find_chd_files()
        if len(uaes) == 0:
            uaes = self.find_uae_files()
        if len(m3us) == 0:
            m3us = self.find_m3u_files()
        if len(zips) == 0:
            zips = self.find_zip_files()
        if len(zs) == 0:
            zs = self.find_zs_files()
        if len(rp9s) == 0:
            rp9s = self.find_rp9_files()

        if len(runs) == 0:
            runs = self.find_run_files()

        if len(adfs) == 0 and len(adzs) == 0 and len(dmss) == 0 and len(fdis) == 0 and len(ipfs) == 0 and len(hdfs) == 0 and len(hdzs) == 0 and len(lhas) == 0 and len(slaves) == 0 and len(infos) == 0 and len(cues) == 0 and len(ccds) == 0 and len(nrgs) == 0 and len(mdss) == 0 and len(isos) == 0 and len(chds) == 0 and len(uaes) == 0 and len(m3us) == 0 and len(zips) == 0 and len(zs) == 0 and len(rp9s) == 0 and len(runs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        # emulator = ['fs-uae', '--fullscreen', '--keep_aspect']
        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('puae_libretro')
        if fullscreen[0] == 'true':
            emulator.append('--fullscreen')

        drives = []
        # Support only one for now..
        if len(exes) > 0:
            emulator = ['fs-uae']
            if emulator[0] == 'fs-uae':
                emulator.append('--hard_drive_0=.')
            if emulator[0] == 'retroarch':
                # emulator.append('--hard_drive_0=.')
                emulator = emulator + [exes[0]]

            if not os.path.exists(self.datadir + "/s"):
                os.makedirs(self.datadir + "/s")
# TODO: when find_files_with_extension works with paths relative to datadir, we can simplify this
                with open(self.datadir + "/s/startup-sequence", 'w') as f:
                    exename = exes[0].split('/')
                    exename = exename[len(exename)-1]
                    f.write(exename + "\n")
                    f.close()
        if len(dmss) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(dmss)
            emulator = emulator + [dmss[0]]
        if len(adfs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(adfs)
            emulator = emulator + [adfs[0]]
        if len(adzs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(adzs)
            emulator = emulator + [adzs[0]]
        if len(fdis) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(fdis)
            emulator = emulator + [fdis[0]]
        if len(ipfs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(ipfs)
            emulator = emulator + [ipfs[0]]
        if len(hdfs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(hdfs)
            emulator = emulator + [hdfs[0]]
        if len(hdzs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(hdzs)
            emulator = emulator + [hdzs[0]]
        if len(lhas) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(lhas)
            emulator = emulator + [lhas[0]]
        if len(slaves) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(slaves)
            emulator = emulator + [slaves[0]]
        if len(infos) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(infos)
            emulator = emulator + [infos[0]]
        if len(cues) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(cues)
            emulator = emulator + [cues[0]]
        if len(ccds) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(ccds)
            emulator = emulator + [ccds[0]]
        if len(nrgs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(nrgs)
            emulator = emulator + [nrgs[0]]
        if len(mdss) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(mdss)
            emulator = emulator + [mdss[0]]
        if len(isos) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(isos)
            emulator = emulator + [isos[0]]
        if len(chds) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(chds)
            emulator = emulator + [chds[0]]
        if len(uaes) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(uaes)
            emulator = emulator + [uaes[0]]
        if len(m3us) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(m3us)
            emulator = emulator + [m3us[0]]
        if len(zips) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(zips)
            emulator = emulator + [zips[0]]
        if len(zs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(zs)
            emulator = emulator + [zs[0]]
        if len(rp9s) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(rp9s)
            emulator = emulator + [rp9s[0]]
        if len(runs) > 0:
            emulator = ['retroarch']
            emulator.append('-L')
            emulator.append('puae_libretro')
            # emulator.append('--fullscreen')
            drives = self.sort_disks(runs)
            emulator = emulator + [runs[0]]

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

    def find_exe_files(self):
        exe_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                exe_files.append(file)
        return exe_files

    def find_dms_files(self):
        dms_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dms_files.append(file)
        return dms_files

    def find_adf_files(self):
        adf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                adf_files.append(file)
        return adf_files

    def find_adz_files(self):
        adz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                adz_files.append(file)
        return adz_files

    def find_fdi_files(self):
        fdi_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                fdi_files.append(file)
        return fdi_files

    def find_ipf_files(self):
        ipf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ipf_files.append(file)
        return ipf_files

    def find_hdf_files(self):
        hdf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                hdf_files.append(file)
        return hdf_files

    def find_hdz_files(self):
        hdz_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                hdz_files.append(file)
        return hdz_files

    def find_lha_files(self):
        lha_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                lha_files.append(file)
        return lha_files

    def find_slave_files(self):
        slave_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                slave_files.append(file)
        return slave_files

    def find_info_files(self):
        info_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                info_files.append(file)
        return info_files

    def find_cue_files(self):
        cue_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                cue_files.append(file)
        return cue_files

    def find_ccd_files(self):
        ccd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ccd_files.append(file)
        return ccd_files

    def find_nrg_files(self):
        nrg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nrg_files.append(file)
        return nrg_files

    def find_mds_files(self):
        mds_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                mds_files.append(file)
        return mds_files

    def find_iso_files(self):
        iso_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                iso_files.append(file)
        return iso_files

    def find_chd_files(self):
        chd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                chd_files.append(file)
        return chd_files

    def find_uae_files(self):
        uae_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                uae_files.append(file)
        return uae_files

    def find_m3u_files(self):
        m3u_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                m3u_files.append(file)
        return m3u_files

    def find_zip_files(self):
        zip_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zip_files.append(file)
        return zip_files

    def find_zs_files(self):
        zs_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                zs_files.append(file)
        return zs_files

    def find_rp9_files(self):
        rp9_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                rp9_files.append(file)
        return rp9_files

    def find_run_files(self):
        run_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                run_files.append(file)
        return run_files
