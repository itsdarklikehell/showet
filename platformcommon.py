import os
import os.path
import inquirer
import subprocess

COREPATH = '/home/rizzo/.config/retroarch/cores'
FULLSCREEN = False
SELECTIVE_MODE = True
DEBUGGING = True


class PlatformCommon:
    prod_files = []
    STEAM = ["False"]
    FULLSCREEN = ["True"]
    NATIVE = ["False"]
    AUDIO = ["True"]
    DEBUGGING = True
    SELECTIVE_MODE = True

    def __init__(self):
        self.showetdir = None
        self.datadir = None
        self.prod_platform = None
        self.prod_files = []

    # TODO: Change this to be relative to datadir
    def find_files_recursively(self, path):
        entries = [os.path.join(path, i) for i in os.listdir(path)]
        if len(entries) == 0:
            return

        for e in entries:
            # check if entry is a file and append it to prod_files.
            if os.path.isfile(e):
                self.prod_files.append(os.path.realpath(e))
            # else check if entry is a directory and find files recursively relative to that path.
            elif os.path.isdir(e):
                self.find_files_recursively(e)

    def setup(self, showetdir, datadir, prod_platform):
        self.showetdir = showetdir
        self.datadir = datadir
        self.prod_platform = prod_platform
        self.find_files_recursively(self.datadir)

    # Returns the list of supported platforms for this platform.
    #
    # Returns:
    #     List of supported platforms.
    def supported_platforms(self):
        """
        Returns the list of supported platforms for this platform.

        Returns:
            List of supported platforms.
        """
        return None

    def find_files_with_extension(self, extension):
        foundfiles = [
            f
            for f in self.prod_files
            if (f.lower().endswith(extension) or f.upper().endswith(extension))
        ]
        return foundfiles

    # Input: list of disk images, output: same list sorted by some
    # logic so that first image is first, second disk then etc..
    def sort_disks(self, files):
        sorted_list = sorted(files, key=lambda s: (s.lower() or s.upper()))
        if len(sorted_list) > 1:
            if DEBUGGING is not False:
                print("\tGuessing disk order should be: ")
                print(sorted_list)
        return sorted_list

    def run_process(self, arguments):
        if DEBUGGING is not False:
            print("\tRunning command: ", arguments)
            print("\t================================")

        process = subprocess.Popen(
            arguments,
            cwd=self.datadir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        process.wait()
        retcode = process.returncode

        for line in process.stdout:
            print(line.decode("utf-8"))
        if retcode:
            if DEBUGGING is not False:
                print(arguments, "\n\tprocess exited with ", retcode)
            exit(-1)
        return retcode

    print("\t================================")

    def multiemu(self, emulators):
        # emulator = []
        if DEBUGGING is not False:
            print("Info: Multiple emulators are supported: " + str(emulators))
        prompt = [
            inquirer.List(
                "emulators",
                message="Please select one of the supported emulators to continue",
                choices=emulators,
            ),
        ]
        emulator = inquirer.prompt(prompt).get("emulators").strip().lower()
        if DEBUGGING is not False:
            print("You chose the selected emulator: " + str(emulator))
        return emulator

    def multicore(self, cores):
        # core = []
        if DEBUGGING is not False:
            print("Info: Multiple cores are supported: " + str(cores))
        prompt = [
            inquirer.List(
                "cores",
                message="Please select one of the supported emulators to continue",
                choices=cores,
            ),
        ]
        core = inquirer.prompt(prompt).get("cores").strip().lower()
        if DEBUGGING is not False:
            print("You chose the selected core: " + str(core))
        return core
