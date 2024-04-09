#!/usr/bin/python3
import os
import json
import argparse
import patoolib
import urllib.request

from platform_3do import Platform_3do
from platform_Amstrad import Platform_Cpcplus
from platform_Apple import Platform_Apple
from platform_Arcade import Platform_Arcade
from platform_Archimedes import Platform_Acorn
from platform_Atari2600 import Platform_Atari2600
from platform_Atari5200 import Platform_Atari5200
from platform_Atari7800 import Platform_Atari7800
from platform_AtariJaguar import Platform_AtariJaguar
from platform_AtariLynx import Platform_AtariLynx
from platform_AtariSTETTFalcon import Platform_AtariSTETTFalcon
from platform_Atarixlxe import Platform_Atarixlxe
from platform_Bandai import Platform_Wonderswan
from platform_Coleco import Platform_Coleco
from platform_Commodore128 import Platform_Commodore128
from platform_Commodore64 import Platform_Commodore64
from platform_CommodoreAmiga import Platform_CommodoreAmiga
from platform_CommodoreCBMII import Platform_CommodoreCBMII
from platform_CommodorePet import Platform_CommodorePet
from platform_CommodorePlus4 import Platform_CommodorePlus4
from platform_CommodoreVic20 import Platform_CommodoreVic20
from platform_Elektronika import Platform_Pdp11
from platform_Enterprise import Platform_Enterprise
from platform_Fairchild import Platform_Channelf
from platform_Gamepark import Platform_GP2X, Platform_GP32
from platform_Gamepark2X import Platform_GP2X
from platform_Gamepark32 import Platform_GP32
from platform_GCE import Platform_Vectrex
from platform_Java import Platform_Java
from platform_Linux import Platform_Linux
from platform_Magnavox import Platform_Odyssey
from platform_Mattel import Platform_Intellivision
from platform_MicrosoftMsx import Platform_Msx
from platform_MicrosoftWindows import Platform_Windows
from platform_MicrosoftXbox import Platform_Xbox
from platform_Nintendo3DS import Platform_3DS
from platform_NintendoDS import Platform_DS
from platform_NintendoFamicom import Platform_Famicom
from platform_NintendoFamicomDisksystem import Platform_FamicomDisksystem
from platform_NintendoGameboy import Platform_Gameboy
from platform_NintendoGameboyAdvance import Platform_GameboyAdvance
from platform_NintendoGameboyColor import Platform_GameboyColor
from platform_NintendoGameCube import Platform_GameCube
from platform_NintendoN64 import Platform_N64
from platform_NintendoPokemini import Platform_Pokemini
from platform_NintendoSuperFamicom import Platform_SuperFamicom
from platform_NintendoVirtualboy import Platform_Virtualboy
from platform_NintendoWii import Platform_Wii
from platform_Palm import Platform_Palm
from platform_Phillips import Platform_Cdi
from platform_Pico8 import Platform_Pico8
from platform_Sega32X import Platform_32X
from platform_SegaDreamcast import Platform_Dreamcast
from platform_SegaGameGear import Platform_GameGear
from platform_SegaMastersystem import Platform_Mastersystem
from platform_SegaMegadrive import Platform_Megadrive
from platform_SegaSaturn import Platform_Saturn
from platform_SegaSG1000 import Platform_SG1000
from platform_SegaStv import Platform_Stv
from platform_SegaVmu import Platform_Vmu
from platform_SinclairSpectrum import Platform_Zxspectrum
from platform_SinclairZx81 import Platform_Zx81
from platform_SnkNeogeo import Platform_Neogeo
from platform_SnkNeogeoPocket import Platform_NeogeoPocket
from platform_SnkNeogeoPocketColor import Platform_NeogeoPocketColor
from platform_SonyPs2 import Platform_Ps2
from platform_SonyPsp import Platform_Psp
from platform_SonyPsx import Platform_Psx
from platform_Spectravideo import Platform_Spectravideo
from platform_Thomson import Platform_MOTO
from platform_Tic80 import Platform_Tic80

from platforms_Atari import (Platform_Atari2600, Platform_Atari5200, Platform_Atari7800,
                             Platform_AtariJaguar, Platform_AtariLynx, Platform_AtariSTETTFalcon, Platform_Atarixlxe)
from platforms_Commodore import (Platform_Commodore128, Platform_Commodore64, Platform_CommodoreAmiga,
                                 Platform_CommodoreCBMII, Platform_CommodorePet, Platform_CommodorePlus4, Platform_CommodoreVic20)
from platform_MicrosoftMsdos import Platform_Msdos
from platforms_Microsoft import (
    Platform_Msx, Platform_Windows, Platform_Xbox, Platform_Msdos)
from platforms_Nec import Platform_Supergrafx
from platforms_Nintendo import (Platform_3DS, Platform_DS, Platform_Famicom, Platform_FamicomDisksystem, Platform_Gameboy, Platform_GameboyAdvance,
                                Platform_GameboyColor, Platform_GameCube, Platform_N64, Platform_Pokemini, Platform_SuperFamicom, Platform_Virtualboy, Platform_Wii)
from platforms_Sega import Platform_32X
from platforms_Sega import (Platform_32X, Platform_Dreamcast, Platform_GameGear, Platform_Vmu,
                            Platform_Mastersystem, Platform_Megadrive, Platform_Saturn, Platform_SG1000, Platform_SG1000, Platform_Stv)
from platforms_Wild import (
    Platform_VideoMPV, Platform_Gamemusic, Platform_VideoFFMPEG)

DEBUGGING = False

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
    Platform_CommodoreAmiga(),
    Platform_Commodore128(),
    Platform_Commodore64(),
    Platform_CommodorePet(),
    Platform_CommodorePlus4(),
    Platform_CommodoreVic20(),
    Platform_CommodoreCBMII(),
    Platform_GameCube(),
    Platform_Wii(),
    Platform_Pokemini(),
    Platform_DS(),
    Platform_3DS(),
    Platform_N64(),
    Platform_SuperFamicom(),
    Platform_Famicom(),
    Platform_FamicomDisksystem(),
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
    Platform_Vmu(),
    Platform_GP32(),
    Platform_GP2X(),
    Platform_Stv(),
    Platform_Neogeo(),
    Platform_NeogeoPocketColor(),
    Platform_NeogeoPocket(),
    Platform_Supergrafx(),
    Platform_Msx(),
    Platform_Xbox(),
    Platform_Mastersystem(),
    Platform_Megadrive(),
    Platform_GameGear(),
    Platform_Dreamcast(),
    Platform_Saturn(),
    Platform_32X(),
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
    Platform_SG1000(),
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
    Platform_Zx81(),
    Platform_Zxspectrum(),
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
prod_url = "http://api.pouet.net/v1/prod/?id=" + str(prod_id)
datadir = showetdir + "/data/" + str(prod_id)
prod_download_url = None
prod_download_filename = None
prod_json = None
prod_json_filename = datadir + "/pouet.json"
if os.path.exists(prod_json_filename):
    if DEBUGGING is not False:
        print("Json already downloaded.")
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
    print("Demo supports platforms ", platforms,
          "of which", prod_platform, "rules the most.")
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
    print("\tPlatform: " + prod_platform)

# Get necessary fields from the data
prod_download_url = data['prod']['download']
prod_download_url = prod_download_url.replace(
    "https://files.scene.org/view", "https://files.scene.org/get")

# Check if the download is already downloaded, else just download it.
if os.path.exists(datadir + "/.FILES_DOWNLOADED"):
    print("\tFile already downloaded")
else:
    if DEBUGGING is not False:
        print("\tDownloading prod file from " + prod_download_url + "...")

    filedata = urllib.request.urlopen(prod_download_url)
    filename = os.path.basename(filedata.url)

    if len(filename) == 0:
        print("Error downloading file at ", prod_download_url)
        exit(-1)
    if DEBUGGING is not False:
        print("\tFilename: ", filename)

    prod_download_filename = datadir + "/" + filename
    datatowrite = filedata.read()

    with open(prod_download_filename, 'wb') as f:
        f.write(datatowrite)

    if DEBUGGING is not False:
        print("\tDownloaded: ", prod_download_filename)
        print("\tFilesize: ", os.path.getsize(prod_download_filename))

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
        if prod_download_filename.endswith(filetype):
            if DEBUGGING is not False:
                print("\t================================")
                print("\tDetected archive: " + filetype)
                print("\t================================")
            extract_files(prod_download_filename, datadir)
            if DEBUGGING is not False:
                print("\t================================")

    # uppercase
    for filetype in filetypes:
        if prod_download_filename.endswith(filetype.upper()):
            if DEBUGGING is not False:
                print("\t================================")
                print("\tDetected archive: " + filetype.upper)
                print("\t================================")
            extract_files(prod_download_filename, datadir)
            if DEBUGGING is not False:
                print("\t================================")

    open(datadir + "/.FILES_DOWNLOADED", 'a').close()

runner.setup(showetdir, datadir, prod_platform)
runner.run()
