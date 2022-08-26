from platformcommon import PlatformCommon
import os

emulator = ['retroarch']
fullscreen = ['false']


class PlatformFamicom(PlatformCommon):
    def run(self):
        extensions = ['nes', 'fds', 'unf', 'unif', 'qd', 'nsf']
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
            emulator.append('quicknes_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")

        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['nesfamicom']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)
        return ext_files


class PlatformSuperFamicom(PlatformCommon):
    def run(self):
        extensions = ['sfc', 'smc', 'fig', 'swc', 'bs']
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
            emulator.append('snes9x_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")

        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['snessuperfamicom']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)
        return ext_files


class PlatformN64(PlatformCommon):
    def run(self):
        extensions = ['n64', 'v64', 'z64', 'bin', 'u1', 'ndd']
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
            emulator.append('parrallel_n64_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")

        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['nintendo64']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)
        return ext_files


class PlatformGameboy(PlatformCommon):
    def run(self):
        extensions = ['gb', 'dmg', 'bin', 'u1', 'ndd', 'zip']
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
            emulator.append('gambatte_libretro')
            # emulator.append('sameboy_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        flipfile = self.datadir + "/fliplist.vfl"
        m3ufile = self.datadir + "/fliplist.m3u"
        with open(flipfile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")
        with open(m3ufile, "w") as f:
            f.write("UNIT 8\n")
            for disk in files:
                f.write(disk + "\n")

        if len(files) > 0:
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gameboy']

# Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json'):
                    ext_files.append(file)
                    print("Found file: " + file)
        return ext_files


class PlatformGameboyColor(PlatformCommon):
    def run(self):
        extensions = ['gbc', 'dmg', 'bin', 'u1', 'ndd']
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
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gambatte_libretro')
            # emulator.append('sameboy_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

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
        extensions = ['gb', 'gbc', 'gba', 'dmg', 'agb', 'bin', 'cgb', 'sgb']
        print("Supported extensions:", extensions)

        # gbs = self.find_files_with_extension('gb')
        # gbcs = self.find_files_with_extension('gbc')
        gbas = self.find_files_with_extension('gba')
        # dmgs = self.find_files_with_extension('dmg')
        # agbs = self.find_files_with_extension('agb')
        # bins = self.find_files_with_extension('bin')
        # cgbs = self.find_files_with_extension('cgb')
        # sgbs = self.find_files_with_extension('sgb')

        # if len(gbs) == 0:
        #     gbs = self.find_gb_files()
        # if len(gbcs) == 0:
        #     gbcs = self.find_gbc_files()
        if len(gbas) == 0:
            gbas = self.find_gba_files()
        # if len(dmgs) == 0:
        #     dmgs = self.find_dmg_files()
        # if len(agbs) == 0:
        #     agbs = self.find_agb_files()
        # if len(bins) == 0:
        #     bins = self.find_bin_files()
        # if len(cgbs) == 0:
        #     cgbs = self.find_cgb_files()
        # if len(sgbs) == 0:
        #     sgbs = self.find_sgb_files()
        if len(gbas) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            # emulator.append('meteor_libretro')
            # emulator.append('vbam_libretro')
            emulator.append('vba_next_libretro')
            # emulator.append('gpsp_libretro')
            # emulator.append('tempgba_libretro')
            # emulator.append('mgba_libretro')
            # emulator.append('mednafen_gba_libretro')
            # emulator.append('sameboy_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        if len(gbas) > 0:
            gbas = self.sort_disks(gbas)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gbas[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gameboyadvance', 'gameboycolor', 'gameboy']

# Tries to identify files by any magic necessary
    def find_gba_files(self):
        gba_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gba_files.append(file)
        return gba_files


class PlatformGamecube(PlatformCommon):
    def run(self):
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        print("Supported extensions:", extensions)

        gcms = self.find_files_with_extension('gcm')

        if len(gcms) == 0:
            gcms = self.find_gcm_files()
        if len(gcms) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('dolphin_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        if len(gcms) > 0:
            gcms = self.sort_disks(gcms)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gcms[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['gamecube']

    def find_gcm_files(self):
        gcm_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gcm_files.append(file)
        return gcm_files


class PlatformWii(PlatformCommon):
    def run(self):
        extensions = ['gcm', 'iso', 'wbfs', 'ciso', 'gcz',
                      'elf', 'dol', 'dff', 'tgc', 'wad', 'rvz', 'm3u']
        print("Supported extensions:", extensions)

        gcms = self.find_files_with_extension('gcm')

        if len(gcms) == 0:
            gcms = self.find_gcm_files()
        if len(gcms) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('dolphin_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        if len(gcms) > 0:
            gcms = self.sort_disks(gcms)
            if emulator[0] == 'retroarch':
                emulator = emulator + [gcms[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['wii', 'wiiu']

    def find_gcm_files(self):
        gcm_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                gcm_files.append(file)
        return gcm_files


class PlatformPokemini(PlatformCommon):
    def run(self):
        extensions = ['min']
        print("Supported extensions:", extensions)

        mins = self.find_files_with_extension('min')

        if len(mins) == 0:
            mins = self.find_min_files()
        if len(mins) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('pokemini_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        if len(mins) > 0:
            mins = self.sort_disks(mins)
            if emulator[0] == 'retroarch':
                emulator = emulator + [mins[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['pokemini']

    def find_min_files(self):
        min_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                min_files.append(file)
        return min_files


class PlatformDS(PlatformCommon):
    def run(self):
        extensions = ['nds', 'dsi']
        print("Supported extensions:", extensions)

        ndss = self.find_files_with_extension('nds')
        dsis = self.find_files_with_extension('dsi')

        if len(ndss) == 0:
            ndss = self.find_nds_files()
        if len(dsis) == 0:
            ndss = self.find_dsi_files()
        if len(ndss) == 0 and len(dsis) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('menlonds_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        if len(ndss) > 0:
            ndss = self.sort_disks(ndss)
            if emulator[0] == 'retroarch':
                emulator = emulator + [ndss[0]]

        if len(dsis) > 0:
            dsis = self.sort_disks(dsis)
            if emulator[0] == 'retroarch':
                emulator = emulator + [dsis[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['nintendods']

    def find_nds_files(self):
        nds_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                nds_files.append(file)
        return nds_files

    def find_dsi_files(self):
        dsi_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                dsi_files.append(file)
        return dsi_files


class PlatformVirtualboy(PlatformCommon):
    def run(self):
        extensions = ['vb', 'vboy', 'bin']
        print("Supported extensions:", extensions)

        vbs = self.find_files_with_extension('vb')
        vboys = self.find_files_with_extension('vboy')
        bins = self.find_files_with_extension('bin')

        if len(vbs) == 0:
            vbs = self.find_vb_files()
        if len(vboys) == 0:
            vboys = self.find_vboy_files()
        if len(bins) == 0:
            bin = self.find_bin_files()
        if len(vbs) == 0 and len(vboys) == 0 and len(bins) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        fullscreen = ['false']
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('mednafen_vb_libretro')
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        if len(vbs) > 0:
            vbs = self.sort_disks(vbs)
            if emulator[0] == 'retroarch':
                emulator = emulator + [vbs[0]]

        if len(vboys) > 0:
            vboys = self.sort_disks(vboys)
            if emulator[0] == 'retroarch':
                emulator = emulator + [vboys[0]]

        if len(bins) > 0:
            bins = self.sort_disks(bins)
            if emulator[0] == 'retroarch':
                emulator = emulator + [bins[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['virtualboy']

    def find_vb_files(self):
        vb_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                vb_files.append(file)
        return vb_files

    def find_vboy_files(self):
        vboy_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                vboy_files.append(file)
        return vboy_files

    def find_bin_files(self):
        bin_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                bin_files.append(file)
        return bin_files
