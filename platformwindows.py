from distutils import extension
from platformcommon import PlatformCommon
from os import listdir
import os.path


class PlatformWindows(PlatformCommon):
    def run(self):
        extensions = ['exe']
        print("Supported extensions:", extensions)

        wineprefix = self.showetdir + '/wineprefix'

        exes = self.find_files_with_extension('exe')

        if len(exes) == 0:
            print("Didn't find any exe files.")
            exit(-1)

        exefile = exes[0]

        print("Guessed executable file: " + exefile)

        exepath = self.datadir + "/" + exefile

        # Setup wine if needed

        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win64" winecfg')

        self.run_process(['wine', exefile])

    def supported_platforms(self):
        return ['windows']
