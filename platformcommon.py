import os
import os.path
from pkgutil import extend_path
import subprocess

class PlatformCommon:
    prod_files = []
    steam = ['false']
    fullscreen = ['true']
    native = ['false']
    audio = ['true']

    debugging = True

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

    def supported_platforms(self):
        return None

    def find_files_with_extension(self, extension):
        foundfiles = [f for f in self.prod_files if (f.lower().endswith(extension) or f.upper().endswith(extension))]
        return foundfiles

    # Input: list of disk images, output: same list sorted by some
    # logic so that first image is first, second disk then etc..
    def sort_disks(self, files):
        sorted_list = sorted(files, key=lambda s: (s.lower() or s.upper()))
        if len(sorted_list) > 1:
            print("\tGuessing disk order should be: ")
            print(sorted_list)
        return sorted_list

    def run_process(self, arguments):
        print("\tRunning command: ", arguments)
        print("\t================================")
        
        process = subprocess.Popen(arguments, cwd=self.datadir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        retcode = process.returncode
        
        for line in process.stdout:
            print(line.decode('utf-8'))
        if retcode:
            print(arguments[0], "\n\tprocess exited with ", retcode)
            exit(-1)
        return retcode
    print("\t================================")
    