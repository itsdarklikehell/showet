import os
from platformcommon import PlatformCommon


class PlatformGamemusic(PlatformCommon):
    emulators = ['retroarch']
    cores = ['gme_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    fullscreen = ['false']
    core = ['gme_libretro']

    def run(self):
        extensions = ['zip', 'ay', 'gbs', 'gym', 'hes',
                      'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['gme_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gme_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

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
        return ['music', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        excl_files = ['.json', '.txt', '.diz']
        for file in self.prod_files:
            if not file.endswith(str(excl_files)):
                size = os.path.getsize(file)
                if size > 0:
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class PlatformVideoFFMPEG(PlatformCommon):
    emulators = ['retroarch']
    cores = ['ffmpeg_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['ffmpeg_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'mkv', 'avi', 'f4v',
                      'f4f', '3gp', 'ogm', 'flv',
                      'mp4', 'mp3', 'flac', 'ogg',
                      'm4a', 'webm', '3g2', 'mov',
                      'wmv', 'mpg', 'mpeg', 'vob',
                      'asf', 'divx', 'm2p', 'm2ts',
                      'ps', 'ts', 'mxf', 'wma',
                      'wav']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['ffmpeg_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('ffmpeg_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

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
        return ['animationvideo', 'linux', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        excl_files = ['.json', '.txt', '.diz']
        for file in self.prod_files:
            if not file.endswith(str(excl_files)):
                size = os.path.getsize(file)
                if size > 0:
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files


class PlatformVideoMPV(PlatformCommon):
    emulators = ['retroarch']
    cores = ['mpv_libretro']
    fullscreens = ['false']

    emulator = ['retroarch']
    core = ['mpv_libretro']
    fullscreen = ['false']

    def run(self):
        extensions = ['zip', 'mkv', 'avi', 'f4v',
                      'f4f', '3gp', 'ogm', 'flv',
                      'mp4', 'mp3', 'flac', 'ogg',
                      'm4a', 'webm', '3g2', 'mov',
                      'wmv', 'mpg', 'mpeg', 'vob',
                      'asf', 'divx', 'm2p', 'm2ts',
                      'ps', 'ts', 'mxf', 'wma',
                      'wav']
        ext = []
        for ext in extensions:
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        emulator = ['retroarch']
        core = ['ffmpeg_libretro']
        fullscreen = ['false']

        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('ffmpeg_libretro')
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        print("\tUsing: " + str(emulator[0]))
        print("\tUsing core: " + str(core[0]))
        print("\tUsing fullscreen: " + str(fullscreen[0]))

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
        return ['animationvideo', 'linux', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        excl_files = ['.json', '.txt', '.diz']
        for file in self.prod_files:
            if not file.endswith(str(excl_files)):
                size = os.path.getsize(file)
                if size > 0:
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
