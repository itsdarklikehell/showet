from platformcommon import PlatformCommon
import os


class PlatformMsdos(PlatformCommon):
    def run(self):
        # executable file types:
        exes = self.find_files_with_extension('exe')
        coms = self.find_files_with_extension('com')
        bats = self.find_files_with_extension('bat')
        confs = self.find_files_with_extension('conf')
        cues = self.find_files_with_extension('cue')
        isos = self.find_files_with_extension('iso')
        # zips = self.find_files_with_extension('zip')

        if len(exes) == 0:
            exes = self.find_exe_files()

        if len(coms) == 0:
            coms = self.find_com_files()

        if len(bats) == 0:
            bats = self.find_bat_files()

        if len(confs) == 0:
            confs = self.find_conf_files()

        if len(cues) == 0:
            cues = self.find_cue_files()

        if len(isos) == 0:
            isos = self.find_iso_files()

        # if len(zips) == 0:
        #     zips = self.find_zip_files()

        if len(exes) == 0 and len(coms) == 0 and len(bats) == 0 and len(confs) == 0 and len(cues) == 0 and len(isos) == 0 and len(zips) == 0:
            print("Didn't find any runable files.")
            exit(-1)

        emulator = ['retroarch']
        emulator.append('-L')
        emulator.append('dosbox_core_libretro')
        # emulator.append('--fullscreen')

        # flipfile = self.datadir + "/fliplist.vfl"
        # with open(flipfile, "w") as f:
        #     f.write("UNIT 8\n")
        #     for disk in exes:
        #         f.write(disk + "\n")
        #     for disk in coms:
        #         f.write(disk + "\n")
        #     for disk in bats:
        #         f.write(disk + "\n")
        #     for disk in confs:
        #         f.write(disk + "\n")
        #     for disk in cues:
        #         f.write(disk + "\n")
        #     for disk in isos:
        #         f.write(disk + "\n")
        #     for disk in zips:
        #         f.write(disk + "\n")

        if len(exes) > 0:
            exes = self.sort_disks(exes)
            emulator = emulator + [exes[0]]
        if len(coms) > 0:
            coms = self.sort_disks(coms)
            emulator = emulator + [coms[0]]
        if len(bats) > 0:
            bats = self.sort_disks(bats)
            emulator = emulator + [bats[0]]
        if len(confs) > 0:
            confs = self.sort_disks(confs)
            emulator = emulator + [confs[0]]
        if len(cues) > 0:
            cues = self.sort_disks(cues)
            emulator = emulator + [cues[0]]
        if len(isos) > 0:
            isos = self.sort_disks(isos)
            emulator = emulator + [isos[0]]
        # if len(zips) > 0:
        #     zips = self.sort_disks(zips)
        #     emulator = emulator + [zips[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['msdos', 'msdosgus']

# Tries to identify files by any magic necessary
    def find_exe_files(self):
        exe_files = []
        for file in self.prod_files:
            exe_files.append(file)
        return exe_files

    def find_com_files(self):
        com_files = []
        for file in self.prod_files:
            com_files.append(file)
        return com_files

    def find_bat_files(self):
        bat_files = []
        for file in self.prod_files:
            bat_files.append(file)
        return bat_files

    def find_conf_files(self):
        conf_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size == 174848:
                conf_files.append(file)
        return conf_files

    def find_cue_files(self):
        cue_files = []
        for file in self.prod_files:
            cue_files.append(file)
        return cue_files

    def find_iso_files(self):
        iso_files = []
        for file in self.prod_files:
            iso_files.append(file)
        return iso_files

    # def find_zip_files(self):
    #     zip_files = []
    #     for file in self.prod_files:
    #         zip_files.append(file)
    #     return zip_files
