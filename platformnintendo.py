from platformcommon import PlatformCommon
import os


class PlatformFamicom(PlatformCommon):
    def run(self):
        extensions = ['nes', 'fds', 'unf', 'unif', 'qd', 'nsf']
        print("Supported extensions:", extensions)

        ness = self.find_files_with_extension('nes')
        fdss = self.find_files_with_extension('fds')
        unfs = self.find_files_with_extension('unf')
        unifs = self.find_files_with_extension('unif')
        qds = self.find_files_with_extension('qd')
        nsfs = self.find_files_with_extension('nsf')

        if len(ness) == 0:
            ness = self.find_nes_files()
        if len(fdss) == 0:
            fdss = self.find_fds_files()
        if len(unfs) == 0:
            unfs = self.find_unf_files()
        if len(unifs) == 0:
            unifs = self.find_unif_files()
        if len(qds) == 0:
            qds = self.find_qd_files()
        if len(nsfs) == 0:
            snfs = self.find_nsf_files()
        if len(ness) == 0 and len(fdss) == 0 and len(ness) == 0 and len(unfs) == 0 and len(unifs) == 0 and len(qds) == 0 and len(nsfs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        # emulator.append('bnes_libretro')
        emulator.append('fixnes_libretro')
        # emulator.append('emux_nes_libretro')
        # emulator.append('nestopia_libretro')
        # emulator.append('--fullscreen')

        if len(ness) > 0:
            ness = self.sort_disks(ness)
            if emulator[0] == 'retroarch':
                emulator = emulator + [ness[0]]

        if len(fdss) > 0:
            fdss = self.sort_disks(fdss)
            if emulator[0] == 'retroarch':
                emulator = emulator + [fdss[0]]

        if len(unfs) > 0:
            unfs = self.sort_disks(unfs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [unfs[0]]

        if len(unifs) > 0:
            unifs = self.sort_disks(unifs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [unifs[0]]

        if len(qds) > 0:
            qds = self.sort_disks(qds)
            if emulator[0] == 'retroarch':
                emulator = emulator + [qds[0]]

        if len(nsfs) > 0:
            nsfs = self.sort_disks(nsfs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [nsfs[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['nesfamicom']

# Tries to identify files by any magic necessary
    def find_fds_files(self):
        fds_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                fds_files.append(file)
        return fds_files

    def find_nes_files(self):
        nes_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nes_files.append(file)
        return nes_files

    def find_unf_files(self):
        unf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                unf_files.append(file)
        return unf_files

    def find_qd_files(self):
        qd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                qd_files.append(file)
        return qd_files

    def find_unif_files(self):
        unif_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                unif_files.append(file)
        return unif_files

    def find_nsf_files(self):
        nsf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nsf_files.append(file)
        return nsf_files


class PlatformSuperFamicom(PlatformCommon):
    def run(self):
        extensions = ['sfc', 'smc', 'fig', 'swc', 'bs', 'gb', 'gbc']
        print("Supported extensions:", extensions)

        sfcs = self.find_files_with_extension('sfc')
        smcs = self.find_files_with_extension('smc')
        figs = self.find_files_with_extension('fig')
        gbcs = self.find_files_with_extension('swc')
        bss = self.find_files_with_extension('bs')
        gbs = self.find_files_with_extension('gb')
        gbcs = self.find_files_with_extension('gbc')

        if len(sfcs) == 0:
            sfcs = self.find_sfc_files()
        if len(smcs) == 0:
            smcs = self.find_smc_files()
        if len(figs) == 0:
            figs = self.find_fig_files()
        if len(gbcs) == 0:
            gbcs = self.find_swc_files()
        if len(bss) == 0:
            bss = self.find_bs_files()
        if len(gbs) == 0:
            gbs = self.find_gb_files()
        if len(gbcs) == 0:
            gbcs = self.find_gbc_files()

        if len(sfcs) == 0 and len(smcs) == 0 and len(sfcs) == 0 and len(figs) == 0 and len(gbcs) == 0 and len(bss) == 0 and len(gbs) == 0 and len(gbcs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        # emulator.append('mesen-s_libretro')
        emulator.append('snes9x_libretro')
        # emulator.append('snes9x2010_libretro')
        # emulator.append('bsnes_hd_beta_libretro)
        # emulator.append('bsnes_cplusplus98_libretro')
        # emulator.append('bsnes2014_balanced_libretro')
        # emulator.append('bsnes_libretro')
        # emulator.append('bsnes_mercury_balanced_libretro')
        # emulator.append('quicknes_libretro')
        # emulator.append('mednafen_snes_libretro')
        # emulator.append('--fullscreen')

        if len(sfcs) > 0:
            sfcs = self.sort_disks(sfcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [sfcs[0]]

        if len(smcs) > 0:
            smcs = self.sort_disks(smcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [smcs[0]]

        if len(figs) > 0:
            figs = self.sort_disks(figs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [figs[0]]

        if len(gbcs) > 0:
            gbcs = self.sort_disks(gbcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbcs[0]]

        if len(bss) > 0:
            bss = self.sort_disks(bss)
            if emulator[0] == 'retroarch':
                emulator = emulator + [bss[0]]

        if len(gbs) > 0:
            gbs = self.sort_disks(gbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbs[0]]

        if len(gbcs) > 0:
            gbcs = self.sort_disks(gbcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbcs[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['snessuperfamicom', 'gameboy']

# Tries to identify files by any magic necessary
    def find_smc_files(self):
        smc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                smc_files.append(file)
        return smc_files

    def find_sfc_files(self):
        sfc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                sfc_files.append(file)
        return sfc_files

    def find_fig_files(self):
        fig_files = []
        for file in self.prod_files:
            fig_files.append(file)
        return fig_files

    def find_swc_files(self):
        swc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                swc_files.append(file)
        return swc_files

    def find_bs_files(self):
        bs_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bs_files.append(file)
        return bs_files

    def find_gb_files(self):
        gb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gb_files.append(file)
        return gb_files

    def find_gbc_files(self):
        gbc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gbc_files.append(file)
        return gbc_files


class PlatformN64(PlatformCommon):
    def run(self):
        extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
        print("Supported extensions:", extensions)

        n64s = self.find_files_with_extension('n64')
        v64s = self.find_files_with_extension('v64')
        z64s = self.find_files_with_extension('z64')
        bins = self.find_files_with_extension('bin')
        u1s = self.find_files_with_extension('u1')
        ndds = self.find_files_with_extension('ndd')

        if len(n64s) == 0:
            n64s = self.find_n64_files()
        if len(v64s) == 0:
            v64s = self.find_v64_files()
        if len(z64s) == 0:
            z64s = self.find_z64_files()
        if len(bins) == 0:
            bins = self.find_bin_files()
        if len(u1s) == 0:
            u1s = self.find_u1s_files()
        if len(ndds) == 0:
            ndds = self.find_ndd_files()

        if len(n64s) == 0 and len(v64s) == 0 and len(n64s) == 0 and len(z64s) == 0 and len(bins) == 0 and len(u1s) == 0 and len(ndds) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        # emulator.append('mupen64plus_next_libretro')
        # emulator.append('mupen64plus_next_gles2_libretro')
        emulator.append('mupen64plus_next_gles3_libretro')
        # emulator.append('mupen64plus_next_develop_libretro')
        # emulator.append('parrallel_n64_libretro')
        # emulator.append('parrallel_n64_debug_libretro')
        # emulator.append('--fullscreen')

        if len(n64s) > 0:
            n64s = self.sort_disks(n64s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [n64s[0]]

        if len(v64s) > 0:
            v64s = self.sort_disks(v64s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [v64s[0]]

        if len(z64s) > 0:
            z64s = self.sort_disks(z64s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [z64s[0]]

        if len(bins) > 0:
            bins = self.sort_disks(bins)
            if emulator[0] == 'retroarch':
                emulator = emulator + [bins[0]]

        if len(u1s) > 0:
            u1s = self.sort_disks(u1s)
            if emulator[0] == 'retroarch':
                emulator = emulator + [u1s[0]]

        if len(ndds) > 0:
            ndds = self.sort_disks(ndds)
            if emulator[0] == 'retroarch':
                emulator = emulator + [ndds[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['nintendo64']

# Tries to identify files by any magic necessary
    def find_v64_files(self):
        v64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                v64_files.append(file)
        return v64_files

    def find_n64_files(self):
        n64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                n64_files.append(file)
        return n64_files

    def find_z64_files(self):
        z64_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                z64_files.append(file)
        return z64_files

    def find_bin_files(self):
        bin_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bin_files.append(file)
        return bin_files

    def find_u1s_files(self):
        u1_files = []
        for file in self.prod_files:
            u1_files.append(file)
        return u1_files

    def find_ndd_files(self):
        ndd_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                ndd_files.append(file)
        return ndd_files


class PlatformGameboy(PlatformCommon):
    def run(self):
        extensions = ['gb', 'gbc', 'dmg', 'bin', 'u1', 'ndd']
        print("Supported extensions:", extensions)

        gbs = self.find_files_with_extension('gb')
        gbcs = self.find_files_with_extension('gbc')
        dmgs = self.find_files_with_extension('dmg')

        if len(gbs) == 0:
            gbs = self.find_gb_files()
        if len(gbcs) == 0:
            gbcs = self.find_gbc_files()
        if len(dmgs) == 0:
            dmgs = self.find_dmg_files()
        if len(gbs) == 0 and len(gbcs) == 0 and len(gbs) == 0 and len(dmgs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('gambatte_libretro')
        # emulator.append('sameboy_libretro')
        # emulator.append('--fullscreen')

        if len(gbs) > 0:
            gbs = self.sort_disks(gbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbs[0]]

        if len(gbcs) > 0:
            gbcs = self.sort_disks(gbcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbcs[0]]

        if len(dmgs) > 0:
            dmgs = self.sort_disks(dmgs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [dmgs[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gameboy', 'gameboycolor']

# Tries to identify files by any magic necessary
    def find_gbc_files(self):
        gbc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gbc_files.append(file)
        return gbc_files

    def find_gb_files(self):
        gb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gb_files.append(file)
        return gb_files

    def find_dmg_files(self):
        dmg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dmg_files.append(file)
        return dmg_files


class PlatformGameboyColor(PlatformCommon):
    def run(self):
        extensions = ['gb', 'gbc', 'dmg', 'bin', 'u1', 'ndd']
        print("Supported extensions:", extensions)

        gbs = self.find_files_with_extension('gb')
        gbcs = self.find_files_with_extension('gbc')
        dmgs = self.find_files_with_extension('dmg')

        if len(gbs) == 0:
            gbs = self.find_gb_files()
        if len(gbcs) == 0:
            gbcs = self.find_gbc_files()
        if len(dmgs) == 0:
            dmgs = self.find_dmg_files()
        if len(gbs) == 0 and len(gbcs) == 0 and len(gbs) == 0 and len(dmgs) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('gambatte_libretro')
        # emulator.append('sameboy_libretro')
        # emulator.append('--fullscreen')

        if len(gbs) > 0:
            gbs = self.sort_disks(gbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbs[0]]

        if len(gbcs) > 0:
            gbcs = self.sort_disks(gbcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbcs[0]]

        if len(dmgs) > 0:
            dmgs = self.sort_disks(dmgs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [dmgs[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gameboy', 'gameboycolor']

# Tries to identify files by any magic necessary
    def find_gbc_files(self):
        gbc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gbc_files.append(file)
        return gbc_files

    def find_gb_files(self):
        gb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gb_files.append(file)
        return gb_files

    def find_dmg_files(self):
        dmg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dmg_files.append(file)
        return dmg_files


class PlatformGameboyAdvance(PlatformCommon):
    def run(self):
        extensions = ['gb', 'gbc', 'gba', 'dmg', 'agb', 'bin']
        print("Supported extensions:", extensions)

        gbs = self.find_files_with_extension('gb')
        gbcs = self.find_files_with_extension('gbc')
        gbcs = self.find_files_with_extension('gba')
        dmgs = self.find_files_with_extension('dmg')
        agbs = self.find_files_with_extension('agb')
        bins = self.find_files_with_extension('bin')

        if len(gbs) == 0:
            gbs = self.find_gb_files()
        if len(gbcs) == 0:
            gbcs = self.find_gbc_files()
        if len(gbas) == 0:
            gbas = self.find_gba_files()
        if len(dmgs) == 0:
            dmgs = self.find_dmg_files()
        if len(agbs) == 0:
            agbs = self.find_agb_files()
        if len(bins) == 0:
            bins = self.find_bin_files()
        if len(gbs) == 0 and len(gbcs) == 0 and len(gbs) == 0 and len(dmgs) == 0 and len(agbs) == 0 and len(bins) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('meteor_libretro')
        # emulator.append('tempgba_libretro')
        # emulator.append('mgba_libretro')
        # emulator.append('mednafen_gba_libretro')
        # emulator.append('sameboy_libretro')

        # emulator.append('--fullscreen')

        if len(gbs) > 0:
            gbs = self.sort_disks(gbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbs[0]]

        if len(gbcs) > 0:
            gbcs = self.sort_disks(gbcs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbcs[0]]

        if len(dmgs) > 0:
            dmgs = self.sort_disks(dmgs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [dmgs[0]]

        if len(agbs) > 0:
            agbs = self.sort_disks(agbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [agbs[0]]

        if len(bins) > 0:
            bins = self.sort_disks(bins)
            if emulator[0] == 'retroarch':
                emulator = emulator + [bins[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gameboy', 'gameboycolor']

# Tries to identify files by any magic necessary
    def find_gbc_files(self):
        gbc_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gbc_files.append(file)
        return gbc_files

    def find_gb_files(self):
        gb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gb_files.append(file)
        return gb_files

    def find_dmg_files(self):
        dmg_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dmg_files.append(file)
        return dmg_files

    def find_agb_files(self):
        agb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                agb_files.append(file)
        return agb_files

    def find_bin_files(self):
        bin_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bin_files.append(file)
        return bin_files
