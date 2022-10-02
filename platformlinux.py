import os
from platformcommon import PlatformCommon


class PlatformLinux(PlatformCommon):
    emulators = ['none']
    cores = ['none']
    fullscreens = ['false']

    emulator = ['none']
    core = ['none']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'exe', 'elf']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['none']
        core = ['none']
        fullscreen = ['false']

        os.chdir(self.datadir)
        if len(files) > 1:
            print("Found multiple executables: ", files,
                  " - not sure which one to run!")
            exit(-1)
        else:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing fullscreen: " + str(fullscreen))

            print("Running ", files[0])
            self.run_process([files[0]])

    def supported_platforms(self):
        return ['linux', 'freebsd']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                if not file.endswith('.json') and not file.endswith('.DIZ'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

