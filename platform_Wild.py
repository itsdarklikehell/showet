import os
import os.path
import stat

from platformcommon import PlatformCommon

fullscreen = False
debugging = True
selective_mode = False

class Platform_Gamemusic(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['gme_libretro']
    extensions = ['zip', 'ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['gme_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['gme_libretro']
        extensions = ['zip', 'ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
                
        if emulator[0] == 'retroarch':
            if core[0] == 'gme_libretro':
                extensions = ['ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz', 'zip']
                
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            with open(flipfile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'music']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'gme_libretro':
                extensions = ['ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz', 'zip']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_VideoFFMPEG(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['ffmpeg_libretro']
    extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['ffmpeg_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['ffmpeg_libretro']
        extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
                
        if emulator[0] == 'retroarch':
            if core[0] == 'ffmpeg_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            with open(flipfile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'ffmpeg_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files

class Platform_VideoMPV(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set whether we should run in fullscreens or not.
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'other']
    cores = ['mpv_libretro']
    extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set whether we should run in fullscreens or not.
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mpv_libretro']
        
        emulators = ['retroarch', 'other']
        cores = ['mpv_libretro']
        extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
                
        if emulator[0] == 'retroarch':
            if core[0] == 'mpv_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions.
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE.
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary.
            files = self.find_ext_files(emulator,core)
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)
        
        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append(core[0])

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'other':
            # Set whether we should run in fullscreens or not.
            if fullscreen == True:
                emulator.append('--fullscreen')

        # print status to console.
        if debugging != False:
            print("\tUsing emulator: " + str(emulator))
            print("\tUsing core: " + str(core))
            print("\tUsing extensions: " + str(extensions))

        if len(files) > 0:
            # Sort the files.
            files = self.sort_disks(files)
            flipfile = self.datadir + "/fliplist.vfl"
            m3ufile = self.datadir + "/fliplist.m3u"
            with open(flipfile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            with open(m3ufile, "w") as f:
                #f.write("UNIT 8\n")
                for disk in files:
                    f.write(disk + "\n")
                f.write("#SAVEDISK:\n")
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['wild', 'animationvideo', 'linux']

    # Tries to identify files by any magic necessary
    def find_ext_files(self,emulator,core):

        if emulator[0] == 'retroarch':
            if core[0] == 'mpv_libretro':
                extensions = ['mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                ext = []
                for ext in extensions:
                    if file.endswith(ext):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
                    if file.endswith(ext.upper()):
                        if debugging != False:
                            print("\tFound file: " + file)
                        os.chmod(file, stat.S_IEXEC)
                        ext_files.append(file)
        return ext_files
