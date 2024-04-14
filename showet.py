#!/usr/bin/python3
import os
import json
import argparse
import os.path
import patoolib
import urllib.request
from 

 
from systems import (Platform_Amstrad_Cpcplus,
                     Platform_Apple_AppleI,
                     Platform_Apple_AppleII,
                     Platform_Apple_AppleIIGS,
                     Platform_Arcade_Arcade,
                     Platform_Archimedes_Acorn,
                     Platform_Atari_2600,
                     Platform_Atari_5200,
                     Platform_Atari_7800,
                     Platform_Atari_Jaguar,
                     Platform_Atari_Lynx,
                     Platform_Atari_STETTFalcon,
                     Platform_Atari_xlxe,
                     Platform_Bandai_Wonderswan,
                     Platform_Coleco_Colecovision,
                     Platform_Commodore_64,
                     Platform_Commodore_128,
                     Platform_Commodore_Amiga,
                     Platform_Commodore_CBMII,
                     Platform_Commodore_Pet,
                     Platform_Commodore_Plus4,
                     Platform_Commodore_Vic20,
                     Platform_Elektronika_Pdp11,
                     Platform_Enterprise_Ep128,
                     Platform_Fairchild_Channelf,
                     Platform_FanCon_Pico8,
                     Platform_FanCon_Tic80,
                     Platform_Gamepark_32,
                     Platform_Gamepark_2X,
                     Platform_GCE_Vectrex,
                     Platform_Java_Java,
                     Platform_Linux_Linux,
                     Platform_Magnavox_Odyssey,
                     Platform_Mattel_Intellivision,
                     Platform_Microsoft_Msx,
                     Platform_Microsoft_Xbox,
                     Platform_Microsoft_Msdos,
                     Platform_Nec_Pcengine,
                     Platform_Nec_Supergrafx,
                     Platform_Nec_Pc8000,
                     Platform_Nec_Pc8800,
                     Platform_Nec_Pc98,
                     Platform_Nec_Pcfx,
                     Platform_Nintendo_3DS,
                     Platform_Nintendo_N64,
                     Platform_Nintendo_DS,
                     Platform_Nintendo_Famicom,
                     Platform_Nintendo_FamicomDisksystem,
                     Platform_Nintendo_Gameboy,
                     Platform_Nintendo_GameboyColor,
                     Platform_Nintendo_GameboyAdvance,
                     Platform_Nintendo_GameCube,
                     Platform_Nintendo_Pokemini,
                     Platform_Nintendo_SuperFamicom,
                     Platform_Nintendo_Virtualboy,
                     Platform_Nintendo_Wii,
                     Platform_Palm_PalmOS,
                     Platform_Panasonic_3do,
                     Platform_Phillips_Cdi,
                     Platform_Sega_32X,
                     Platform_Sega_Dreamcast,
                     Platform_Sega_GameGear,
                     Platform_Sega_Mastersystem,
                     Platform_Sega_Megadrive,
                     Platform_Sega_Saturn,
                     Platform_Sega_Stv,
                     Platform_Sega_Vmu,
                     Platform_Sega_SG1000,
                     Platform_Sinclair_Zxspectrum,
                     Platform_Sinclair_Zx81,
                     Platform_Snk_Neogeo,
                     Platform_Snk_NeogeoPocket,
                     Platform_Snk_NeogeoPocketColor,
                     Platform_Sony_Ps2,
                     Platform_Sony_Psp,
                     Platform_Sony_Psx,
                     Platform_SpectraVision_SpectraVideo,
                     Platform_Thomson_MOTO,
                     Platform_Wild_Gamemusic,
                     Platform_Wild_VideoFFMPEG,
                     Platform_Wild_VideoMPV)


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
    Platform_Coleco_Colecovision(),
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
    Platform_FanCon_Tic80(),
    Platform_Gamepark_32(),
    Platform_Gamepark_2X(),
    Platform_GCE_Vectrex(),
    Platform_Java_Java(),
    Platform_Linux_Linux(),
    Platform_Magnavox_Odyssey(),
    Platform_Mattel_Intellivision(),
    Platform_Microsoft_Msx(),
    Platform_Microsoft_Xbox(),
    Platform_Microsoft_Msdos(),
    Platform_Nec_Pcengine(),
    Platform_Nec_Supergrafx(),
    Platform_Nec_Pc8000(),
    Platform_Nec_Pc8800(),
    Platform_Nec_Pc98(),
    Platform_Nec_Pcfx(),
    Platform_Nintendo_3DS(),
    Platform_Nintendo_N64(),
    Platform_Nintendo_DS(),
    Platform_Nintendo_Famicom(),
    Platform_Nintendo_FamicomDisksystem(),
    Platform_Nintendo_Gameboy(),
    Platform_Nintendo_GameboyColor(),
    Platform_Nintendo_GameboyAdvance(),
    Platform_Nintendo_GameCube(),
    Platform_Nintendo_Pokemini(),
    Platform_Nintendo_SuperFamicom(),
    Platform_Nintendo_Virtualboy(),
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
    Platform_Sega_Stv(),
    Platform_Sega_Vmu(),
    Platform_Sega_SG1000(),
    Platform_Sinclair_Zxspectrum(),
    Platform_Sinclair_Zx81(),
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
