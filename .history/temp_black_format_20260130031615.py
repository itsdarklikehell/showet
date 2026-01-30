#!/usr/bin/python3
import os
import json
import argparse
# import os.path
import urllib.request
import patoolib

from Platform_Amstrad_Cpcplus import Platform_Amstrad_Cpcplus
from Platform_Apple_AppleI import Platform_Apple_AppleI
from Platform_Apple_AppleII import Platform_Apple_AppleII
from Platform_Apple_AppleIIGS import Platform_Apple_AppleIIGS
from Platform_Arcade_Arcade import Platform_Arcade_Arcade
from Platform_Archimedes_Acorn import Platform_Archimedes_Acorn
from Platform_Atari_2600 import Platform_Atari_2600
from Platform_Atari_5200 import Platform_Atari_5200
from Platform_Atari_7800 import Platform_Atari_7800
from Platform_Atari_Jaguar import Platform_Atari_Jaguar
from Platform_Atari_Lynx import Platform_Atari_Lynx
from Platform_Atari_STETTFalcon import Platform_Atari_STETTFalcon
from Platform_Atari_xlxe import Platform_Atari_xlxe
from Platform_Bandai_Wonderswan import Platform_Bandai_Wonderswan
from Platform_Commodore_64 import Platform_Commodore_64
from Platform_Commodore_128 import Platform_Commodore_128
from Platform_Commodore_Amiga import Platform_Commodore_Amiga
from Platform_Commodore_CBMII import Platform_Commodore_CBMII
from Platform_Commodore_Pet import Platform_Commodore_Pet
from Platform_Commodore_Plus4 import Platform_Commodore_Plus4
from Platform_Commodore_Vic20 import Platform_Commodore_Vic20
from Platform_Elektronika_Pdp11 import Platform_Elektronika_Pdp11
from Platform_Enterprise_Ep128 import Platform_Enterprise_Ep128
from Platform_Fairchild_Channelf import Platform_Fairchild_Channelf
from Platform_FanCon_Pico8 import Platform_FanCon_Pico8
from Platform_Gamepark_2X import Platform_Gamepark_2X
from Platform_Gamepark_32 import Platform_Gamepark_32
from Platform_GCE_Vectrex import Platform_GCE_Vectrex
from Platform_Java_Java import Platform_Java_Java
from Platform_Linux_Linux import Platform_Linux_Linux
from Platform_Magnavox_Odyssey import Platform_Magnavox_Odyssey
from Platform_Mattel_Intellivision import Platform_Mattel_Intellivision
from Platform_Microsoft_Msdos import Platform_Microsoft_Msdos
from Platform_Microsoft_Msx import Platform_Microsoft_Msx
from Platform_Microsoft_Windows import Platform_Microsoft_Windows
from Platform_Microsoft_Xbox import Platform_Microsoft_Xbox
from Platform_Nec_Pc98 import Platform_Nec_Pc98
from Platform_Nec_Pc8000 import Platform_Nec_Pc8000
from Platform_Nec_Pc8800 import Platform_Nec_Pc8800
from Platform_Nec_Pcengine import Platform_Nec_Pcengine
from Platform_Nec_Pcfx import Platform_Nec_Pcfx
from Platform_Nec_Supergrafx import Platform_Nec_Supergrafx
from Platform_Nintendo_3DS import Platform_Nintendo_3DS
from Platform_Nintendo_Famicom import Platform_Nintendo_Famicom
from Platform_Nintendo_FamicomDisksystem import Platform_Nintendo_FamicomDisksystem
from Platform_Nintendo_Gameboy import Platform_Nintendo_Gameboy
from Platform_Nintendo_GameboyAdvance import Platform_Nintendo_GameboyAdvance
from Platform_Nintendo_GameboyColor import Platform_Nintendo_GameboyColor
from Platform_Nintendo_GameCube import Platform_Nintendo_GameCube
from Platform_Nintendo_N64 import Platform_Nintendo_N64
from Platform_Nintendo_Pokemini import Platform_Nintendo_Pokemini
from Platform_Nintendo_SuperFamicom import Platform_Nintendo_SuperFamicom
from Platform_Nintendo_Wii import Platform_Nintendo_Wii
from Platform_Palm_PalmOS import Platform_Palm_PalmOS
from Platform_Panasonic_3do import Platform_Panasonic_3do
from Platform_Phillips_Cdi import Platform_Phillips_Cdi
from Platform_Sega_32X import Platform_Sega_32X
from Platform_Sega_Dreamcast import Platform_Sega_Dreamcast
from Platform_Sega_GameGear import Platform_Sega_GameGear
from Platform_Sega_Mastersystem import Platform_Sega_Mastersystem
from Platform_Sega_Megadrive import Platform_Sega_Megadrive
from Platform_Sega_Saturn import Platform_Sega_Saturn
from Platform_Sega_SG1000 import Platform_Sega_SG1000
from Platform_Sega_Stv import Platform_Sega_Stv
from Platform_Sega_Vmu import Platform_Sega_Vmu
from Platform_Sinclair_Zx81 import Platform_Sinclair_Zx81
from Platform_Sinclair_Zxspectrum import Platform_Sinclair_Zxspectrum
from Platform_Snk_Neogeo import Platform_Snk_Neogeo
from Platform_Snk_NeogeoPocket import Platform_Snk_NeogeoPocket
from Platform_Snk_NeogeoPocketColor import Platform_Snk_NeogeoPocketColor
from Platform_Sony_Ps2 import Platform_Sony_Ps2
from Platform_Sony_Psp import Platform_Sony_Psp
from Platform_Sony_Psx import Platform_Sony_Psx
from Platform_SpectraVision_SpectraVideo import Platform_SpectraVision_SpectraVideo
from Platform_Thomson_MOTO import Platform_Thomson_MOTO
from Platform_Wild_Gamemusic import Platform_Wild_Gamemusic
from Platform_Wild_VideoFFMPEG import Platform_Wild_VideoFFMPEG
from Platform_Wild_VideoMPV import Platform_Wild_VideoMPV

COREPATH = '/home/rizzo/.config/retroarch/cores'
FULLSCREEN = False
DEBUGGING = True

parser = argparse.ArgumentParser(description='Show a demo on screen.')
parser.add_argument('pouetid', type=int, nargs='?',
                    help='Pouet ID of the production to show')
parser.add_argument('--platforms', action="store_true",
                    help='List supported platforms and exit')
parser.add_argument('--random', action="store_true",
                    help='Play random productions')

args = parser.parse_args()

# In priority order
platform_runners = [
    Platform_Amstrad_Cpcplus(),
    Platform_Apple_AppleI(),
    Platform_Apple_AppleII(),
    Platform_Apple_AppleIIGS(),
    Platform_Arcade_Arcade(),
    Platform_Archimedes_Acorn(),
    Platform_Atari_2600(),
    Platform_Atari_5200(),
    Platform_Atari_7800(),
    Platform_Atari_Jaguar(),
    Platform_Atari_Lynx(),
    Platform_Atari_STETTFalcon(),
    Platform_Atari_xlxe(),
    Platform_Bandai_Wonderswan(),
    Platform_Commodore_64(),
    Platform_Commodore_128(),
    Platform_Commodore_Amiga(),
    Platform_Commodore_CBMII(),
    Platform_Commodore_Pet(),
    Platform_Commodore_Plus4(),
    Platform_Commodore_Vic20(),
    Platform_Elektronika_Pdp11(),
    Platform_Enterprise_Ep128(),
    Platform_Fairchild_Channelf(),
    Platform_FanCon_Pico8(),
    Platform_Gamepark_2X(),
    Platform_Gamepark_32(),
    Platform_GCE_Vectrex(),
    Platform_Java_Java(),
    Platform_Linux_Linux(),
    Platform_Magnavox_Odyssey(),
    Platform_Mattel_Intellivision(),
    Platform_Microsoft_Msdos(),
    Platform_Microsoft_Msx(),
    Platform_Microsoft_Windows(),
    Platform_Microsoft_Xbox(),
    Platform_Nec_Pc98(),
    Platform_Nec_Pc8000(),
    Platform_Nec_Pc8800(),
    Platform_Nec_Pcengine(),
    Platform_Nec_Pcfx(),
    Platform_Nec_Supergrafx(),
    Platform_Nintendo_3DS(),
    Platform_Nintendo_Famicom(),
    Platform_Nintendo_FamicomDisksystem(),
    Platform_Nintendo_Gameboy(),
    Platform_Nintendo_GameboyAdvance(),
    Platform_Nintendo_GameboyColor(),
    Platform_Nintendo_GameCube(),
    Platform_Nintendo_N64(),
    Platform_Nintendo_Pokemini(),
    Platform_Nintendo_SuperFamicom(),
    Platform_Nintendo_Wii(),
    Platform_Palm_PalmOS(),
    Platform_Panasonic_3do(),
    Platform_Phillips_Cdi(),
    Platform_Sega_32X(),
    Platform_Sega_Dreamcast(),
    Platform_Sega_GameGear(),
    Platform_Sega_Mastersystem(),
    Platform_Sega_Megadrive(),
    Platform_Sega_Saturn(),
    Platform_Sega_SG1000(),
    Platform_Sega_Stv(),
    Platform_Sega_Vmu(),
    Platform_Sinclair_Zx81(),
    Platform_Sinclair_Zxspectrum(),
    Platform_Snk_Neogeo(),
    Platform_Snk_NeogeoPocket(),
    Platform_Snk_NeogeoPocketColor(),
    Platform_Sony_Ps2(),
    Platform_Sony_Psp(),
    Platform_Sony_Psx(),
    Platform_SpectraVision_SpectraVideo(),
    Platform_Thomson_MOTO(),
    Platform_Wild_Gamemusic(),
    Platform_Wild_VideoFFMPEG(),
    Platform_Wild_VideoMPV()
]

if args.platforms:
    for r in platform_runners:
        for p in r.supported_platforms():
            print(p)
    exit(0)

showetdir = os.path.expanduser("~/.showet")

if not args.pouetid:
    print("No pouet id specified. Use --help to see options.")
    exit(-1)

# Get the json data:
prod_id = args.pouetid
PROD_URL = "http://api.pouet.net/v1/prod/?id=" + str(prod_id)
datadir = showetdir + "/data/" + str(prod_id)
PROD_DOWNLOAD_URL = None
PROD_DOWNLOAD_FILENAME = None
PROD_JSON = None
PROD_JSON_FILENAME = datadir + "/pouet.json"
if os.path.exists(PROD_JSON_FILENAME):
    if DEBUGGING is not False:
        print("Json already downloaded.")
    with open(PROD_JSON_FILENAME, 'r') as f:
        PROD_JSON = f.read()
else:
    if not os.path.exists(datadir + '/json'):
        os.makedirs(datadir + '/json')
    with urllib.request.urlopen(PROD_URL) as url:
        PROD_JSON = url.read().decode()
    with open(PROD_JSON_FILENAME, 'w') as f:
        f.write(PROD_JSON)
        f.close()

# print(prod_json)
data = json.loads(PROD_JSON)

PROD_PLATFORM = None
RUNNER = None
platforms = []
for p in data['prod']['platforms'].values():
    platforms.append(p['slug'])

for prunner in platform_runners:
    for demoplat in platforms:
        if PROD_PLATFORM is None and demoplat in prunner.supported_platforms():
            PROD_PLATFORM = demoplat
            RUNNER = prunner

if not RUNNER:
    print("ERROR: Platform " + str(platforms) + " not supported (yet!).")
    exit(-1)

if len(platforms) > 1:
    print("Demo supports platforms ", platforms,
          "of which", PROD_PLATFORM, "rules the most.")
    # Should be possible to implement a inquirer menu here but this ^ works for now.

# Print fields collected from the data:
# Name: + data['prod']['name']
# By: " + data['prod']['groups'][0]['name']
# Type: " + data['prod']['type']
# Released: " + data['prod']['releaseDate']
# Platform: " + prod_platform
if DEBUGGING is not False:
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
    print("\tPlatform: " + PROD_PLATFORM)

# Get necessary fields from the data
PROD_DOWNLOAD_URL = data['prod']['download']
PROD_DOWNLOAD_URL = PROD_DOWNLOAD_URL.replace(
    "https://files.scene.org/view", "https://files.scene.org/get")

# Check if the download is already downloaded, else just download it.
if os.path.exists(datadir + "/.FILES_DOWNLOADED"):
    print("\tFile already downloaded")
else:
    if DEBUGGING is not False:
        print("\tDownloading prod file from " + PROD_DOWNLOAD_URL + "...")

    filedata = urllib.request.urlopen(PROD_DOWNLOAD_URL)
    filename = os.path.basename(filedata.url)

    if len(filename) == 0:
        print("Error downloading file at ", PROD_DOWNLOAD_URL)
        exit(-1)
    if DEBUGGING is not False:
        print("\tFilename: ", filename)

    PROD_DOWNLOAD_FILENAME = datadir + "/" + filename
    datatowrite = filedata.read()

    with open(PROD_DOWNLOAD_FILENAME, 'wb') as f:
        f.write(datatowrite)

    if DEBUGGING is not False:
        print("\tDownloaded: ", PROD_DOWNLOAD_FILENAME)
        print("\tFilesize: ", os.path.getsize(PROD_DOWNLOAD_FILENAME))

    # extract files depending on the filetype
    def extract_files(prod_download_filename, datadir):
        if not prod_download_filename.endswith("exe") or not prod_download_filename.endswith("EXE"):
            patoolib.extract_archive(
                prod_download_filename, outdir=datadir, verbosity=1, interactive=None)
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

    # lowercase
    for filetype in filetypes:
        if PROD_DOWNLOAD_FILENAME.endswith(filetype):
            if DEBUGGING is not False:
                print("\t================================")
                print("\tDetected archive: " + filetype)
                print("\t================================")
            extract_files(PROD_DOWNLOAD_FILENAME, datadir)
            if DEBUGGING is not False:
                print("\t================================")

    # uppercase
    for filetype in filetypes:
        if PROD_DOWNLOAD_FILENAME.endswith(filetype.upper()):
            if DEBUGGING is not False:
                print("\t================================")
                print("\tDetected archive: " + filetype.upper)
                print("\t================================")
            extract_files(PROD_DOWNLOAD_FILENAME, datadir)
            if DEBUGGING is not False:
                print("\t================================")

    open(datadir + "/.FILES_DOWNLOADED", 'a').close()

RUNNER.setup(showetdir, datadir, PROD_PLATFORM)
RUNNER.run()

