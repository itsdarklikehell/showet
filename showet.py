#!/usr/bin/python3
import urllib.request
import json
import os
import argparse
import patoolib
import inquirer

from platform_3do import Platform_3do
from platform_Amstrad import Platform_Cpcplus
from platform_Apple import Platform_Apple
from platform_Arcade import Platform_Arcade
from platform_Archimedes import Platform_Acorn
from platform_Atari import (
    Platform_Atarixlxe,
    Platform_AtariSTETTFalcon,
    Platform_AtariJaguar,
    Platform_AtariLynx,
    Platform_Atari2600,
    Platform_Atari5200,
    Platform_Atari7800 
)
from platform_Bandai import Platform_Wonderswan
from platform_Coleco import Platform_Coleco
from platform_Commodore import (
    Platform_Commodore64,
    Platform_CommodorePet,
    Platform_Commodore128,
    Platform_CommodorePlus4,
    Platform_CommodoreVIC20,
    Platform_CommodoreCBMII,
    Platform_CommodoreAmiga
)
from platform_Dos import Platform_Msdos
from platform_Elektronika import Platform_Pdp11
from platform_Enterprise import Platform_Enterprise
from platform_Fairchild import Platform_Channelf
from platform_GCE import Platform_Vectrex
from platform_Java import Platform_Java
from platform_Linux import Platform_Linux
from platform_Magnavox import Platform_Odyssey
from platform_Mattel import Platform_Intellivision
from platform_Microsoft import (
    Platform_Windows,
    Platform_Msx,
    Platform_Xbox
)
from platform_Nec import Platform_Supergrafx
from platform_Nintendo import (
    Platform_Gameboy,
    Platform_GameboyColor,
    Platform_GameboyAdvance,
    Platform_Famicom,
    Platform_SuperFamicom, 
    Platform_Virtualboy,
    Platform_N64,
    Platform_Gamecube,
    Platform_Wii,
    Platform_Pokemini,
    Platform_DS
)
from platform_Palm import Platform_Palm
from platform_Phillips import Platform_Cdi
from platform_Pico8 import Platform_Pico8
from platform_Sega import (
    Platform_Megadrive,
    Platform_Gamegear,
    Platform_Mastersystem,
    Platform_Dreamcast,
    Platform_Saturn
)
#from platform_Sinclair import (
#    Platform_Zxspectrum,
#    Platform_Zx81
#)
from platform_Snk import (
    Platform_Neogeo,
    Platform_Neopocket,
    Platform_Neopocketcolor
)
from platform_Sony import (
    Platform_Psx,
    Platform_Psp,
    Platform_Ps2
)
from platform_Spectravideo import Platform_Spectravideo
from platform_Tic80 import Platform_Tic80
from platform_Gamepark import (
    Platform_GP2x,
    Platform_GP32
)
from platform_Thomson import Platform_MOTO
from platform_Wild import (
    Platform_Gamemusic,
    Platform_VideoMPV,
    Platform_VideoFFMPEG
)

debugging = True

parser = argparse.ArgumentParser(description='Show a demo on screen.')
parser.add_argument('pouetid', type=int, nargs='?', help='Pouet ID of the production to show')
parser.add_argument('--platforms', action="store_true", help='List supported platforms and exit')
parser.add_argument('--random', action="store_true", help='Play random productions')

args = parser.parse_args()

# In priority order
platform_runners = [
    Platform_CommodoreAmiga(),
    Platform_Commodore128(),
    Platform_Commodore64(), 
    Platform_CommodorePet(),
    Platform_CommodorePlus4(),
    Platform_CommodoreVIC20(),
    Platform_CommodoreCBMII(),
    Platform_Gamecube(),
    Platform_Wii(),
    Platform_Pokemini(),
    Platform_DS(),
    Platform_N64(),
    Platform_SuperFamicom(),
    Platform_Famicom(),
    Platform_GameboyAdvance(),
    Platform_GameboyColor(),
    Platform_Gameboy(),
    Platform_Virtualboy(),
    Platform_Ps2(),
    Platform_Psp(),
    Platform_Psx(),
    Platform_Apple(),
    Platform_Tic80(),
    Platform_MOTO(),
    Platform_GP32(),
    Platform_GP2x(),
    Platform_Neogeo(),
    Platform_Neopocketcolor(),
    Platform_Neopocket(),
    Platform_Supergrafx(),
    Platform_Msx(),
    Platform_Xbox(),
    Platform_Mastersystem(),
    Platform_Megadrive(),
    Platform_Gamegear(),
    Platform_Dreamcast(),
    Platform_Saturn(),
    Platform_Intellivision(),
    Platform_Java(),
    Platform_Acorn(),
    Platform_Palm(),
    Platform_Pico8(),
    Platform_Vectrex(),
    Platform_Pdp11(),
    Platform_Gamemusic(),
    Platform_VideoMPV(),
    Platform_VideoFFMPEG(),
    Platform_Arcade(),
    Platform_3do(),
    Platform_Wonderswan(), 
    Platform_Coleco(),
    Platform_Channelf(),
    Platform_Odyssey(),
    Platform_Cdi(), 
    Platform_Spectravideo(),
    Platform_AtariSTETTFalcon(),
    Platform_Atarixlxe(), 
    Platform_AtariJaguar(),
    Platform_AtariLynx(),
    Platform_Atari2600(),
    Platform_Atari5200(),
    Platform_Atari7800(),
    Platform_Enterprise(),
    Platform_Cpcplus(),
    Platform_Linux(),
    Platform_Msdos(),
    Platform_Windows(),
    ]
    #Platform_Zxspectrum(),
    #Platform_Zx81(),
if args.platforms:
    for r in platform_runners:
        for p in r.supported_platforms():
            print(p)
    exit(0)

showetdir = os.path.expanduser("~/.showet")
RetroPieEmuDir = os.path.expanduser("/opt/retropie/emulators")

print("Check: If Folder %s exists." % showetdir)
if not os.path.exists(showetdir):
    print("Warning: Folder %s does not exist" % showetdir)
    os.makedirs(showetdir)
    print("Info: Folder %s Created." % showetdir)
else:
    print("Info: Folder %s exists." % showetdir)

print("Check: if Folder %s exists." % RetroPieEmuDir)
if not os.path.exists(RetroPieEmuDir):
    print("Warning: %s does not exist" % RetroPieEmuDir)
    #exit(-1)
else:
    print("Info: Folder %s exists." % RetroPieEmuDir)


if not args.pouetid:
    print("No pouet id specified. Use --help to see options.")
    exit(-1)

# Get the json data:
prod_id = args.pouetid
prod_url = "http://api.pouet.net/v1/prod/?id=" + str(prod_id)
datadir = showetdir + "/data/" + str(prod_id)
prod_download_url = None
prod_download_filename = None
prod_json = None
prod_json_filename = datadir + "/pouet.json"
if os.path.exists(prod_json_filename):
    if debugging != False:
        print("Json already downloaded")
    with open(prod_json_filename, 'r') as f:
        prod_json = f.read()
else:
    if not os.path.exists(datadir + '/json'):
        os.makedirs(datadir + '/json')
    with urllib.request.urlopen(prod_url) as url:
        prod_json = url.read().decode()
    with open(prod_json_filename, 'w') as f:
        f.write(prod_json)
        f.close()

# print(prod_json)
data = json.loads(prod_json)

prod_platform = None
runner = None
platforms = []
for p in data['prod']['platforms'].values():
    platforms.append(p['slug'])

for prunner in platform_runners:
    for demoplat in platforms:
        if prod_platform is None and demoplat in prunner.supported_platforms():
            prod_platform = demoplat
            runner = prunner

if not runner:
    print("ERROR: Platform " + str(platforms) + " not supported (yet!).")
    exit(-1)

if len(platforms) > 1:
    print("Demo supports platforms ", platforms, "of which", prod_platform, "rules the most.")
    # Should be possible to implement a inquirer menu here but this ^ works for now.

# Print fields collected from the data:
# Name: + data['prod']['name']
# By: " + data['prod']['groups'][0]['name']
# Type: " + data['prod']['type']
# Released: " + data['prod']['releaseDate']
# Platform: " + prod_platform
if debugging != False:
    print("\tName: " + data['prod']['name'])
    try:
        print("\tBy: " + data['prod']['groups'][0]['name'])
    except IndexError:
        pass
    try:
        print("\tType: " + data['prod']['type'])
    except IndexError:
        pass    
    # try:
    #     print("\tReleased: " + data['prod']['releaseDate'])
    # except IndexError:
    #     pass
    print("\tPlatform: " + prod_platform)

# Get necessary fields from the data
prod_download_url = data['prod']['download']
prod_download_url = prod_download_url.replace("https://files.scene.org/view", "https://files.scene.org/get")

# Check if the download is already downloaded, else just download it.
if os.path.exists(datadir + "/.FILES_DOWNLOADED"):
        print("\tFile already downloaded")
else:
    if debugging != False:
        print("\tDownloading prod file from " + prod_download_url + "...")
    
    filedata = urllib.request.urlopen(prod_download_url)
    filename = os.path.basename(filedata.url)
    
    if len(filename) == 0:
        print("Error downloading file at ", prod_download_url)
        exit(-1)
    if debugging != False:
        print("\tFilename: ", filename)

    prod_download_filename = datadir + "/" + filename
    datatowrite = filedata.read()

    with open(prod_download_filename, 'wb') as f:
        f.write(datatowrite)

    if debugging != False:
        print("\tDownloaded: ", prod_download_filename)
        print("\tFilesize: ", os.path.getsize(prod_download_filename))

    # extract files depending on the filetype
    def extract_files(prod_download_filename, datadir):
        if not prod_download_filename.endswith("exe") or not prod_download_filename.endswith("EXE"):
            patoolib.extract_archive(prod_download_filename, outdir=datadir, verbosity=0, interactive=None)
            os.system("tochd -d " + datadir + " -- " + prod_download_filename)
            os.system("tochd -q -d " + datadir + " " + datadir)
    filetypes = [
        '7z',
        'ap_',
        'apk',
        'ar',
        'arc',
        'arj',
        'bz',
        'bz2',
        'cab',
        'cb7',
        'crx',
        'dazip',
        'deb',
        'dmg',
        'gnutar',
        'gz',
        'gzi',
        'gzip',
        'hfs',
        'iso',
        'jgz',
        'lha',
        'lxf',
        'lhz',
        'lzma',
        'mcgame',
        'mct',
        'mcworld',
        'msi',
        'ntfs',
        'pax',
        'pet',
        'pk3',
        'psz',
        'r00',
        'rar',
        'reloc',
        'sdt',
        'sdz',
        'sdz',
        'sfs',
        'sfx',
        'spk',
        'squashfs',
        'tar',
        'tar.gz',
        'tar.gz2',
        'tar.lzma',
        'tar.xz',
        'tbz',
        'tgz',
        't64.gz',
        'tlz',
        'u3p',
        'udf',
        'vhd',
        'wim',
        'xar',
        'xz',
        'zad',
        'zip',
        '001',
        '7z.001',
        '7z.002',
        'azw2',
        'he',
        'r01',
        'r02',
        'r03',
        'r21',
        'txz',
        'zi',
        'zpi',
        ] 
    filetype = []
    #lowercase
    for filetype in filetypes:
        if prod_download_filename.endswith(filetype):
            if debugging != False:
                print("\t================================")
                print("\tDetected archive: " + filetype)
                print("\t================================")
            extract_files(prod_download_filename, datadir)
            if debugging != False:
                print("\t================================")
    #uppercase
    for filetype in filetypes:
        if prod_download_filename.endswith(filetype.upper()):
            if debugging != False:

                print("\t================================")
                print("\tDetected archive: " + filetype)
                print("\t================================")
            extract_files(prod_download_filename, datadir)
            if debugging != False:
                print("\t================================")
    
    open(datadir + "/.FILES_DOWNLOADED", 'a').close()

runner.setup(showetdir, datadir, prod_platform)
runner.run()
