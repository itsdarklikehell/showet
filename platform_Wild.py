import os
import os.path
from platformcommon import PlatformCommon

class Platform_Gamemusic(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['gme_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['gme_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'ay', 'gbs', 'gym', 'hes', 'kss', 'nsf', 'nsfe', 'sap', 'spc', 'vgm', 'vgz']
        
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary    
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('gme_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'vlc':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
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
            # Sort the files.
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['music', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.ay') or file.endswith('.gbs') or file.endswith('.gym') or file.endswith('.hes') or file.endswith('.kss') or file.endswith('.nsf') or file.endswith('.nsfe') or file.endswith('.sap') or file.endswith('.spc') or file.endswith('.vgm') or file.endswith('.vgz'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.AY') or file.endswith('.GBS') or file.endswith('.GYM') or file.endswith('.HES') or file.endswith('.KSS') or file.endswith('.NSF') or file.endswith('.NSFE') or file.endswith('.SAP') or file.endswith('.SPC') or file.endswith('.VGM') or file.endswith('.VGZ'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_VideoFFMPEG(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['ffmpeg_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['ffmpeg_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary    
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)

        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('ffmpeg_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'vlc':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
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
            # Sort the files.
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == 'vlc':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['animationvideo', 'linux', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.mkv') or file.endswith('.avi') or file.endswith('.f4v') or file.endswith('.f4f') or file.endswith('.3gp') or file.endswith('.ogm') or file.endswith('.flv') or file.endswith('.mp4') or file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.ogg') or file.endswith('.m4a') or file.endswith('.webm') or file.endswith('.3g2') or file.endswith('.mov') or file.endswith('.wmv') or file.endswith('.mpg') or file.endswith('.mpeg') or file.endswith('.vob') or file.endswith('.asf') or file.endswith('.divx') or file.endswith('.m2p') or file.endswith('.m2ts') or file.endswith('.ps') or file.endswith('.ts') or file.endswith('.mxf') or file.endswith('.wav'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.MKV') or file.endswith('.AVI') or file.endswith('.F4V') or file.endswith('.F4F') or file.endswith('.3GP') or file.endswith('.OGM') or file.endswith('.FLV') or file.endswith('.MP4') or file.endswith('.MP3') or file.endswith('.FLAC') or file.endswith('.OGG') or file.endswith('.M4A') or file.endswith('.WEBM') or file.endswith('.3G2') or file.endswith('.MOV') or file.endswith('.WMV') or file.endswith('.MPG') or file.endswith('.MPEG') or file.endswith('.VOB') or file.endswith('.ASF') or file.endswith('.DIVX') or file.endswith('.M2P') or file.endswith('.M2TS') or file.endswith('.PS') or file.endswith('.TS') or file.endswith('.MXF') or file.endswith('.WAV'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_VideoMPV(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['mpv_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['ffmpeg_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'mkv', 'avi', 'f4v', 'f4f', '3gp', 'ogm', 'flv', 'mp4', 'mp3', 'flac', 'ogg', 'm4a', 'webm', '3g2', 'mov', 'wmv', 'mpg', 'mpeg', 'vob', 'asf', 'divx', 'm2p', 'm2ts', 'ps', 'ts', 'mxf', 'wma', 'wav']
        
        ext = []
        for ext in extensions:
            # Tries to identify files by the list of extensions
            files = self.find_files_with_extension(ext)
        if len(files) == 0:
            # Tries to identify files by the list of extensions in UPPERCASE
            files = self.find_files_with_extension(ext.upper())
        if len(files) == 0:
            # Tries to identify files by any magic necessary    
            files = self.find_ext_files()
        if len(files) == 0:
            print("Didn't find any runnable files.")
            exit(-1)
        
        # in case we are running retroarch, we need to provide some arguments to set the libretro core (fullpath or shortname).
        if emulator[0] == 'retroarch':
            emulator.append('-L')
            emulator.append('ffmpeg_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'vlc':
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # print status to console.
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
            # Sort the files.
            files = self.sort_disks(files)
            if emulator[0] == 'retroarch':
                emulator = emulator + [files[0]]
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['animationvideo', 'linux', 'wild']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.mkv') or file.endswith('.avi') or file.endswith('.f4v') or file.endswith('.f4f') or file.endswith('.3gp') or file.endswith('.ogm') or file.endswith('.flv') or file.endswith('.mp4') or file.endswith('.mp3') or file.endswith('.flac') or file.endswith('.ogg') or file.endswith('.m4a') or file.endswith('.webm') or file.endswith('.3g2') or file.endswith('.mov') or file.endswith('.wmv') or file.endswith('.mpg') or file.endswith('.mpeg') or file.endswith('.vob') or file.endswith('.asf') or file.endswith('.divx') or file.endswith('.m2p') or file.endswith('.m2ts') or file.endswith('.ps') or file.endswith('.ts') or file.endswith('.mxf') or file.endswith('.wav'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.MKV') or file.endswith('.AVI') or file.endswith('.F4V') or file.endswith('.F4F') or file.endswith('.3GP') or file.endswith('.OGM') or file.endswith('.FLV') or file.endswith('.MP4') or file.endswith('.MP3') or file.endswith('.FLAC') or file.endswith('.OGG') or file.endswith('.M4A') or file.endswith('.WEBM') or file.endswith('.3G2') or file.endswith('.MOV') or file.endswith('.WMV') or file.endswith('.MPG') or file.endswith('.MPEG') or file.endswith('.VOB') or file.endswith('.ASF') or file.endswith('.DIVX') or file.endswith('.M2P') or file.endswith('.M2TS') or file.endswith('.PS') or file.endswith('.TS') or file.endswith('.MXF') or file.endswith('.WAV'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
