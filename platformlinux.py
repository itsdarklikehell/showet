from platformcommon import PlatformCommon
import os
import stat


class PlatformLinux(PlatformCommon):
    def run(self):
        exes = self.find_exe_files()
        elfs = self.find_elf_files()

        if len(exes) == 0 and len(elfs) == 0:
            print("Didn't find any runnable binaries.")
            exit(-1)

        os.chdir(self.datadir)
        if len(exes) > 1:
            print("Found executables: ", exes, " - not sure which one to run!")
            exit(-1)
        else:
            print("Running ", exes[0])
            self.run_process([exes[0]])

        if len(elfs) > 1:
            print("Found ELFs: ", elfs, " - not sure which one to run!")
            exit(-1)
        else:
            print("Running ", elfs[0])
            self.run_process([elfs[0]])

    def supported_platforms(self):
        return ['linux']

# Tries to identify d64 files by any magic necessary
    def find_exe_files(self):
        exe_files = []
        for exe_files in self.prod_files:
            mode = os.stat(exe_files).st_mode
            if stat.S_IXUSR & mode:
                exe_files.append(exe_files)
        return exe_files

    def find_elf_files(self):
        elf_files = []
        for elf_files in self.prod_files:
            mode = os.stat(elf_files).st_mode
            if stat.S_IXUSR & mode:
                elf_files.append(elf_files)
        return elf_files
