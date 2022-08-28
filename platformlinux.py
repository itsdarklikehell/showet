from platformcommon import PlatformCommon
import os
import stat

fullscreen = ['true']


class PlatformLinux(PlatformCommon):
    def run(self):
        extensions = ['.exe', '.elf']
        ext = []
        for ext in extensions:
            print("looking for files ending with: " + ext)
            files = self.find_files_with_extension(ext)

        if len(files) == 0:
            files = self.find_ext_files()

        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        os.chdir(self.datadir)
        if len(files) > 1:
            print("Found multiple executables: ", files,
                  " - not sure which one to run!")
            exit(-1)
        else:
            print("Running ", files[0])
            self.run_process([files[0]])

    def supported_platforms(self):
        return ['linux', 'freebsd']


# Tries to identify files by any magic necessary


    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0 and not file.endswith('.json'):
                ext_files.append(file)
                print("Found file: " + file)
        return ext_files
