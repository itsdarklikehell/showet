#!/usr/bin/python3
import urllib.request
import json
import os
import argparse
from platform_3do import Platform_3do
from platform_Amstrad import Platform_Caprice, Platform_Crocods
from platform_Apple import Platform_Apple
from platform_Arcade import Platform_Arcade
from platform_Archimedes import Platform_Acorn
from platform_Atari import Platform_Atarixlxe, Platform_AtariSTETTFalcon, Platform_AtariJaguar, Platform_AtariLynx, Platform_Atari2600, Platform_Atari5200
from platform_Bandai import Platform_Wonderswan
from platform_Coleco import Platform_Coleco
from platform_Commodore import Platform_Commodore64, Platform_CommodorePet, Platform_Commodore128, Platform_CommodorePlus4, Platform_CommodoreVIC20, Platform_CommodoreCBMII, Platform_CommodoreAmiga
from platform_Dos import Platform_Msdos
from platform_Elektronika import Platform_Pdp11
from platform_Enterprise import Platform_Enterprise
from platform_Fairchild import Platform_Channelf
from platform_GCE import Platform_Vectrex
from platform_Java import Platform_Java
from platform_Linux import Platform_Linux
from platform_Magnavox import Platform_Odyssey
from platform_Mattel import Platform_Intellivision
from platform_Microsoft import Platform_Windows, Platform_Msx, Platform_Xbox
from platform_Nec import Platform_Supergrafx
from platform_Nintendo import Platform_Gameboy, Platform_GameboyColor, Platform_GameboyAdvance, Platform_Famicom, Platform_SuperFamicom, Platform_Virtualboy, Platform_N64, Platform_Gamecube, Platform_Wii, Platform_Pokemini, Platform_DS
from platform_Palm import Platform_Palm
from platform_Phillips import Platform_Cdi
from platform_Pico8 import Platform_Pico8
from platform_Sega import Platform_Megadrive, Platform_Gamegear, Platform_Mastersystem, Platform_Genesis, Platform_Dreamcast, Platform_Saturn
from platform_Sinclair import Platform_Zx81, Platform_Zxspectrum
from platform_Snk import Platform_Neogeo, Platform_Neopocket, Platform_Neopocketcolor
from platform_Sony import Platform_Psx, Platform_Psp, Platform_Ps2
from platform_Spectravideo import Platform_Spectravideo
from platform_Tic80 import Platform_Tic80
from platform_Wild import Platform_Gamemusic, Platform_VideoMPV, Platform_VideoFFMPEG


parser = argparse.ArgumentParser(description='Show a demo on screen.')
parser.add_argument('pouetid', type=int, nargs='?',
                    help='Pouet ID of the production to show')
parser.add_argument('--platforms', action="store_true",
                    help='List supported platforms and exit')
parser.add_argument('--random', action="store_true",
                    help='Play random productions')

args = parser.parse_args()

# In priority order
platform_runners = [Platform_Caprice(), Platform_Crocods(), Platform_Famicom(),
                    Platform_SuperFamicom(), Platform_N64(), Platform_Gameboy(),
                    Platform_GameboyColor(), Platform_GameboyAdvance(),
                    Platform_Zx81(), Platform_Zxspectrum(),
                    Platform_Commodore64(), Platform_CommodoreAmiga(), Platform_CommodorePet(), Platform_Commodore128(),
                    Platform_CommodorePlus4(), Platform_CommodoreVIC20(), Platform_CommodoreCBMII(),
                    Platform_Gamecube(), Platform_Wii(), Platform_Pokemini(), Platform_DS(),
                    Platform_Virtualboy(), Platform_Windows(), Platform_Msdos(), Platform_Linux(),
                    Platform_Apple(), Platform_Tic80(), Platform_Neogeo(), Platform_Neopocket(),
                    Platform_Neopocketcolor(), Platform_Supergrafx(), Platform_Msx(), Platform_Xbox(),
                    Platform_Gamegear(), Platform_Mastersystem(), Platform_Megadrive(),
                    Platform_Genesis(), Platform_Saturn(), Platform_Enterprise(), Platform_Psx(),
                    Platform_Ps2(), Platform_Psp(), Platform_Intellivision(), Platform_Java(),
                    Platform_Acorn(), Platform_Palm(), Platform_Pico8(), Platform_Vectrex(),
                    Platform_Dreamcast(), Platform_Pdp11(), Platform_Gamemusic(), Platform_VideoMPV(),
                    Platform_VideoFFMPEG(), Platform_Arcade(), Platform_3do(), Platform_Wonderswan(), 
                    Platform_Coleco(), Platform_Channelf(), Platform_Odyssey(), Platform_Cdi(), 
                    Platform_Spectravideo(), Platform_AtariSTETTFalcon(), Platform_Atarixlxe(), 
                    Platform_AtariJaguar(), Platform_AtariLynx(), Platform_Atari2600(), Platform_Atari5200(),]

if args.platforms:
    for r in platform_runners:
        for p in r.supported_platforms():
            print(p)
    exit(0)

showetdir = os.path.expanduser("~/.showet")

if not os.path.exists(showetdir):
    os.makedirs(showetdir)

if not args.pouetid:
    print("No pouet id specified. Use --help to see options.")
    exit(-1)

prod_id = args.pouetid
prod_url = "http://api.pouet.net/v1/prod/?id=" + str(prod_id)
datadir = showetdir + "/data/" + str(prod_id)
prod_download_url = None
prod_download_filename = None
prod_json = None
prod_json_filename = datadir + "/pouet.json"

# Get the json data:
if os.path.exists(prod_json_filename):
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
    print("Demo supports platform platforms ", platforms,
          "of which", prod_platform, "rules the most.")

print("\tName: " + data['prod']['name'])
try:
    print("\tBy: " + data['prod']['groups'][0]['name'])
except IndexError:
    pass
print("\tType: " + data['prod']['type'])
# print("\tReleased: " + data['prod']['releaseDate'])
print("\tPlatform: " + prod_platform)

# Get necessary fields from the data

prod_download_url = data['prod']['download']
prod_download_url = prod_download_url.replace(
    "https://files.scene.org/view", "https://files.scene.org/get")

if os.path.exists(datadir + "/.FILES_DOWNLOADED"):
    print("\tFile already downloaded")
else:
    print("\n\tDownloading prod file from " + prod_download_url + "...")
    filedata = urllib.request.urlopen(prod_download_url)
    filename = os.path.basename(filedata.url)
    if len(filename) == 0:
        print("Error downloading file at ", prod_download_url)
        exit(-1)
    print("\n\tFilename: ", filename)
    prod_download_filename = datadir + "/" + filename
    datatowrite = filedata.read()

    with open(prod_download_filename, 'wb') as f:
        f.write(datatowrite)

    print("\tDownloaded: ", prod_download_filename,
          "\n\tFilesize: ", os.path.getsize(prod_download_filename))

    # Decompress the file if needed
    # if prod_download_filename.endswith(".lha"):
    #     print("\tExtracting:", prod_download_filename, "To:", datadir)
    #     ret = os.system("lhasa x " + datadir + " " + prod_download_filename)
    #     if ret == 1:
    #         print("\tExtracting file failed!")

    if prod_download_filename.endswith(".7z"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("7z x " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".zip"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("unzip -u -d " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".tar.bz2"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xjvf " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".tar.gz"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xzvf " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".bz2"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("bunzip2 " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".rar"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("7z x " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".gz"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("gunzip " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".tar"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xf " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".tbz2"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xjvf " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".tgz"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xzvf " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".7z"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("7z x " + datadir + " " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")

    if prod_download_filename.endswith(".arc"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("arc x " + prod_download_filename + " " + datadir)
        #ret = os.system("nomarch " + prod_download_filename + " " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
    
    if prod_download_filename.endswith(".arj"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("arj x " + datadir + " " + prod_download_filename)
        #ret = os.system("nomarch " + prod_download_filename + " " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    open(datadir + "/.FILES_DOWNLOADED", 'a').close()

runner.setup(showetdir, datadir, prod_platform)
runner.run()
