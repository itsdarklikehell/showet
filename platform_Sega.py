import os
import os.path
from platformcommon import PlatformCommon

class Platform_32X(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'picodrive']
    cores = ['picodrive_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['picodrive_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'bin', 'gen', 'gg', 'smd', 'pco', 'md', '32x', 'chd', 'cue', 'iso', 'sms', '68k', 'sgd', 'm3u']
        
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
            emulator.append('picodrive_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['sega32x']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.bin') or file.endswith('.gen') or file.endswith('.gg') or file.endswith('.smd') or file.endswith('.pco') or file.endswith('.md') or file.endswith('.32x') or file.endswith('.chd') or file.endswith('.cue') or file.endswith('.iso') or file.endswith('.sms') or file.endswith('.68k') or file.endswith('.sgd') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.BIN') or file.endswith('.GEN') or file.endswith('.GG') or file.endswith('.SMD') or file.endswith('.PCO') or file.endswith('.MD') or file.endswith('.32X') or file.endswith('.CHD') or file.endswith('.CUE') or file.endswith('.ISO') or file.endswith('.SMS') or file.endswith('.68K') or file.endswith('.SGD') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                
        return ext_files

class Platform_Dreamcast(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch']
    cores = ['flycast_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'chd', 'cdi', 'iso', 'elf', 'bin', 'cue', 'gdi', 'lst', 'dat', '7z', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['flycast_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'chd', 'cdi', 'iso', 'elf', 'bin', 'cue', 'gdi', 'lst', 'dat', '7z', 'm3u']
        
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
            emulator.append('flycast_libretro')
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
        return ['dreamcast']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.chd') or file.endswith('.cdi') or file.endswith('.iso') or file.endswith('.elf') or file.endswith('.bin') or file.endswith('.cue') or file.endswith('.gdi') or file.endswith('.lst') or file.endswith('.dat') or file.endswith('.7z') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.CHD') or file.endswith('.CDI') or file.endswith('.ISO') or file.endswith('.ELF') or file.endswith('.BIN') or file.endswith('.CUE') or file.endswith('.GDI') or file.endswith('.LST') or file.endswith('.DAT') or file.endswith('.7Z') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_Gamegear(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    fullscreens = ['false']
    cores = ['gearsystem_libretro', 'genesis_plus_gx_libretro', 'fbneo_gg_libretro']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['gearsystem_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
    
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
            emulator.append('gearsystem_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagamegear']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.sms') or file.endswith('.gg') or file.endswith('.sg') or file.endswith('.bin') or file.endswith('.rom'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.SMS') or file.endswith('.GG') or file.endswith('.SG') or file.endswith('.BIN') or file.endswith('.ROM'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                
        return ext_files

class Platform_Mastersystem(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'osmose']
    cores = ['genesis_plus_gx_libretro', 'fbneo_sms_libretro', 'gearsystem_libretro', 'picodrive_libretro', 'smsplus_gx_libreto']
    fullscreens = ['false']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['genesis_plus_gx_libretro']        
        fullscreen = ['false']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
        
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
            emulator.append('genesis_plus_gx_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segamastersystem', 'segagamegear', 'segasg1000', 'segagenesismegadrive', 'segasaturn', 'segastv']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.mdx') or file.endswith('.md') or file.endswith('.smd') or file.endswith('.gen') or file.endswith('.bin') or file.endswith('.cue') or file.endswith('.iso') or file.endswith('.sms') or file.endswith('.bms') or file.endswith('.gg') or file.endswith('.sg') or file.endswith('.68k') or file.endswith('.sgd') or file.endswith('.chd') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.MDX') or file.endswith('.MD') or file.endswith('.SMD') or file.endswith('.GEN') or file.endswith('.BIN') or file.endswith('.CUE') or file.endswith('.ISO') or file.endswith('.SMS') or file.endswith('.BMS') or file.endswith('.GG') or file.endswith('.SG') or file.endswith('.68K') or file.endswith('.SGD') or file.endswith('.CHD') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
        return ext_files

class Platform_Megadrive(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'dgen']
    cores = ['genesis_plus_gx_libretro', 'fbneo_md_libretro', 'picodrive_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['picodrive_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'mdx', 'md', 'smd', 'gen', 'bin', 'cue', 'iso', 'sms', 'bms', 'gg', 'sg', '68k', 'sgd', 'chd', 'm3u']

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
            emulator.append('picodrive_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segagenesismegadrive']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.mdx') or file.endswith('.md') or file.endswith('.smd') or file.endswith('.gen') or file.endswith('.bin') or file.endswith('.cue') or file.endswith('.iso') or file.endswith('.sms') or file.endswith('.bms') or file.endswith('.gg') or file.endswith('.sg') or file.endswith('.68k') or file.endswith('.sgd') or file.endswith('.chd') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.MDX') or file.endswith('.MD') or file.endswith('.SMD') or file.endswith('.GEN') or file.endswith('.BIN') or file.endswith('.CUE') or file.endswith('.ISO') or file.endswith('.SMS') or file.endswith('.BMS') or file.endswith('.GG') or file.endswith('.SG') or file.endswith('.68K') or file.endswith('.SGD') or file.endswith('.CHD') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)            
        return ext_files

class Platform_Saturn(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    fullscreens = ['false']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['mednafen_saturn_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
        
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
            emulator.append('mednafen_saturn_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasaturn']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.sms') or file.endswith('.gg') or file.endswith('.sg') or file.endswith('.bin') or file.endswith('.rom'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.SMS') or file.endswith('.GG') or file.endswith('.SG') or file.endswith('.BIN') or file.endswith('.ROM'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_Stv(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'yabause', 'kronos']
    cores = ['yabause_libretro', 'kronos_libretro', 'mednafen_saturn_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['kronos_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'ccd', 'chd', 'cue', 'iso', 'mds', 'm3u']
        
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
            emulator.append('kronos_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segastv']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.ccd') or file.endswith('.chd') or file.endswith('.cue') or file.endswith('.iso') or file.endswith('.mds') or file.endswith('.m3u'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.CCD') or file.endswith('.CHD') or file.endswith('.CUE') or file.endswith('.ISO') or file.endswith('.MDS') or file.endswith('.M3U'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_Vmu(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'vemulator']
    cores = ['vemulator_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'vms', 'dci', 'bin']
    
    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        fullscreen = ['false']
        core = ['vemulator_libretro']
        extensions = ['zip', 'vms', 'dci', 'bin']
        
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
            emulator.append('vemulator_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segavmu']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.vms') or file.endswith('.dci') or file.endswith('.bin'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.VMS') or file.endswith('.DCI') or file.endswith('.BIN'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files

class Platform_SG1000(PlatformCommon):
    # Set up the emulator we want to run.
    # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
    # Set wether we should run in fullscreens or not.        
    # Supply A list of extensions that the specified emulator supports.
    emulators = ['retroarch', 'gearsystem']
    cores = ['gearsystem_libretro']
    fullscreens = ['false']
    extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']

    def run(self):
        # Set up the emulator we want to run.
        # in case we are running retroarch, we need to set the libretro core (fullpath or shortname).
        # Set wether we should run in fullscreens or not.        
        # Supply A list of extensions that the specified emulator supports.
        emulator = ['retroarch']
        core = ['gearsystem_libretro']
        fullscreen = ['false']
        extensions = ['zip', 'sms', 'gg', 'sg', 'bin', 'rom']
        
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
            emulator.append('bluemsx_libretro')
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
            if emulator[0] == '3do':
                emulator = emulator + ['-flipname', flipfile, files[0]]

        self.run_process(emulator)

    def supported_platforms(self):
        return ['segasg1000']

    # Tries to identify files by any magic necessary
    def find_ext_files(self):
        ext_files = []
        for file in self.prod_files:
            size = os.path.getsize(file)
            if size > 0:
                # Tries to exclude files that end with certain extensions/we dont need.. Grrgrrgll.
                if file.endswith('.zip') or file.endswith('.sms') or file.endswith('.gg') or file.endswith('.sg') or file.endswith('.bin') or file.endswith('.rom'):
                #if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.TXT') and not file.endswith('.diz') and not file.endswith('.DIZ') and not file.endswith('.nfo') and not file.endswith('.NFO') and not file.endswith('.png') and not file.endswith('.PNG') and not file.endswith('.jpg') and not file.endswith('.JPG') and not file.endswith('.org') and not file.endswith('.ORG') and not file.endswith('.org.txt'):
                    ext_files.append(file)
                    print("\tFound file: " + file)
                if file.endswith('.ZIP') or file.endswith('.SMS') or file.endswith('.GG') or file.endswith('.SG') or file.endswith('.BIN') or file.endswith('.ROM'):
                    ext_files.append(file)
                    print("\tFound file: " + file)                    
        return ext_files
