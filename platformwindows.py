from platformcommon import PlatformCommon
from os import listdir
import os.path


class PlatformWindows(PlatformCommon):
    def run(self):
        wineprefix = self.showetdir + '/wineprefix'

        exefiles = self.find_files_with_extension('exe')
        batfiles = self.find_files_with_extension('bat')

        if len(exefiles) == 0:
            print("Didn't find any exe files.")
            exit(-1)

        if len(batfiles) == 0:
            print("Didn't find any bat files.")
            exit(-1)

        exefile = exefiles[0]
        batfile = batfiles[0]

        print("Guessed executable file: " + exefile)
        print("Guessed batch file: " + batfile)

        exepath = self.datadir + "/" + exefile
        batpath = self.datadir + "/" + batfile

        # Setup wine if needed

        os.putenv("WINEPREFIX", wineprefix)

        if not os.path.exists(wineprefix):
            os.makedirs(wineprefix)
            print("Creating wine prefix: " + str(wineprefix))
            os.system('WINEARCH="win32" winecfg')

        self.run_process(['wine', batfile])
        self.run_process(['wine', exefile])

    def supported_platforms(self):
        return ['windows']
