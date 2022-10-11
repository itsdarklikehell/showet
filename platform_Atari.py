import os
import os.path
from platformcommon import PlatformCommon

class Platform_AtariSTETTFalcon(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'stella', 'hatari']
    cores = ['hatari_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['hatari_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'st', 'msa', 'stx', 'dim', 'ipf', 'm3u']
        
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
            emulator.append('hatari_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'hatari':
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
            if emulator[0] == 'hatari':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarifalcon030', 'atarist', 'atariste', 'ataritt030']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.st') or file.endswith('.msa') or file.endswith('.stx') or file.endswith('.dim') or file.endswith('.ipf') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.ST') or file.endswith('.MSA') or file.endswith('.STX') or file.endswith('.DIM') or file.endswith('.IPF') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Atarixlxe(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['atari800_libretro']
    fullscreens = ['false']
    extensions = ['st', 'msa', 'zip', 'stx', 'dim', 'ipf', 'm3u', 'xex']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['atari800_libretro']
        fullscreen = ['false']
        extensions = ['st', 'msa', 'zip', 'stx', 'dim', 'ipf', 'm3u', 'xex']

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
        if emulator[0] == ['retroarch']:
            emulator.append('-L')
            emulator.append('atari800_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == 'true':
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
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
            if emulator[0] == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.st') or file.endswith('.msa') or file.endswith('.stx') or file.endswith('.dim') or file.endswith('.ipf') or file.endswith('.m3u') or file.endswith('.xex'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_AtariJaguar(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['virtualjaguar_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.        
        emulator = ['retroarch']
        core = ['virtualjaguar_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'j64', 'jag', 'rom', 'abs', 'cof', 'bin', 'prg']
        
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
            emulator.append('virtualjaguar_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'virtualjaguar':
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
            if emulator[0] == 'virtualjaguar':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarijaguar']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.j64') or file.endswith('.jag') or file.endswith('.rom') or file.endswith('.abs') or file.endswith('.cof') or file.endswith('.bin') or file.endswith('.prg'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_AtariLynx(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.

    emulators = ['retroarch', 'mednafen']
    cores = ['handy_libretro', 'mednafen_lynx_libretro']
    fullscreens = ['false']
    extensions = ['lnx', 'o']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['mednafen_lynx_libretro']
        extensions = ['lnx', 'o']

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
            emulator.append('mednafen_lynx_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
                
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'mednafen':
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
            if emulator[0] == 'mednafen':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarilynx']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.lnx') or file.endswith('.o'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Atari2600(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'stella']
    cores = ['stella2014_libretro', 'stella_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'a26', 'bin']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['stella2014_libretro', 'stella_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'a26', 'bin']
        
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
            emulator.append('stella2014_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
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
            if emulator[0] == '4do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarivcs']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.a26') or file.endswith('.bin'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Atari5200(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'atari800']
    cores = ['atari800_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['atari800_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'xfd', 'atr', 'cdm', 'cas', 'bin', 'a52', 'atx', 'car', 'rom', 'com', 'xex']
        
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
            emulator.append('atari800_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')

        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == 'atari800':
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
            if emulator[0] == 'atari800':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['atarixlxe']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.xfd') or file.endswith('.atr') or file.endswith('.cdm') or file.endswith('.cas') or file.endswith('.bin') or file.endswith('.a52') or file.endswith('.atx') or file.endswith('.car') or file.endswith('.rom') or file.endswith('.xex'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Atari7800(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'prosystem']
    cores = ['prosystem_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'a78', 'bin', 'cdf']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['prosystem_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'a78', 'bin', 'cdf']
        
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
            emulator.append('prosystem_libretro')
            # Set wether we should run in fullscreens or not.
            if fullscreen == ['true']:
                emulator.append('--fullscreen')
        
        # in case we are not running retroarch, and we need to provide some arguments to the emulator we can do so here:
        if emulator[0] == '4do':
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
            if emulator[0] == '4do':
                emulator = emulator + ['-flipname', flipfile, files[0]]
                
        self.run_process(emulator)

    def supported_platforms(self):
        return ['atari7800']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.a78') or file.endswith('.bin') or file.endswith('.cdf'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files
