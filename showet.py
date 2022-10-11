#!/usr/bin/python3
import urllib.request
import json
import os
import argparse
from platform_3do import Platform_3do
from platform_Amstrad import Platform_Cpcplus
from platform_Apple import Platform_Apple
from platform_Arcade import Platform_Arcade
from platform_Archimedes import Platform_Acorn
from platform_Atari import Platform_Atarixlxe, Platform_AtariSTETTFalcon, Platform_AtariJaguar, Platform_AtariLynx, Platform_Atari2600, Platform_Atari5200, Platform_Atari7800
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
from platform_Sega import Platform_Megadrive, Platform_Gamegear, Platform_Mastersystem, Platform_Dreamcast, Platform_Saturn
from platform_Sinclair import Platform_Zxspectrum
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
platform_runners = [Platform_Cpcplus(),
                    Platform_Famicom(),
                    Platform_SuperFamicom(),
                    Platform_N64(),
                    Platform_Gameboy(),
                    Platform_GameboyColor(),
                    Platform_GameboyAdvance(),
                    Platform_Zxspectrum(),
                    Platform_Commodore64(), 
                    Platform_CommodoreAmiga(),
                    Platform_CommodorePet(),
                    Platform_Commodore128(),
                    Platform_CommodorePlus4(),
                    Platform_CommodoreVIC20(),
                    Platform_CommodoreCBMII(),
                    Platform_Gamecube(),
                    Platform_Wii(),
                    Platform_Pokemini(),
                    Platform_DS(),
                    Platform_Virtualboy(),
                    Platform_Msdos(),
                    Platform_Windows(),
                    Platform_Linux(),
                    Platform_Apple(),
                    Platform_Tic80(),
                    Platform_Neogeo(),
                    Platform_Neopocket(),
                    Platform_Neopocketcolor(),
                    Platform_Supergrafx(),
                    Platform_Msx(),
                    Platform_Xbox(),
                    Platform_Gamegear(),
                    Platform_Mastersystem(),
                    Platform_Megadrive(),
                    Platform_Saturn(),
                    Platform_Enterprise(),
                    Platform_Psx(),
                    Platform_Ps2(),
                    Platform_Psp(),
                    Platform_Intellivision(),
                    Platform_Java(),
                    Platform_Acorn(),
                    Platform_Palm(),
                    Platform_Pico8(),
                    Platform_Vectrex(),
                    Platform_Dreamcast(),
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
                    Platform_Atari7800()]

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

    # Decompress the file if needed:
    
    # lzh
    if prod_download_filename.endswith(".lzh") or prod_download_filename.endswith(".LZH") or prod_download_filename.endswith(".lzs") or prod_download_filename.endswith(".LZS") or prod_download_filename.endswith(".pma") or prod_download_filename.endswith(".PMA"):
        print("\tExtracting:", prod_download_filename, "To:", datadir)
        ret = os.system("lhasa x " + prod_download_filename + " " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    # rar
    if prod_download_filename.endswith(".rar") or prod_download_filename.endswith(".RAR"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("rar x " + prod_download_filename + " " + datadir + " >/dev/null 2>&1")
        if ret == 1:
            print("\tExtracting file failed!")
            
    # 7zip,zip    
    if prod_download_filename.endswith(".7z") or prod_download_filename.endswith(".7Z") or prod_download_filename.endswith(".zip") or prod_download_filename.endswith(".ZIP"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("7za e -y '" + prod_download_filename + "' -o" + datadir + " >/dev/null 2>&1")
        if ret == 1:
            print("\tExtracting file failed!")
            
    # tar,bz2
    if prod_download_filename.endswith(".tar") or prod_download_filename.endswith(".TAR") or prod_download_filename.endswith(".bz2") or prod_download_filename.endswith(".BZ2") or prod_download_filename.endswith(".tar.bz2") or prod_download_filename.endswith(".TAR.BZ2") or prod_download_filename.endswith(".tbz2") or prod_download_filename.endswith(".TBZ2"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xjvf " + prod_download_filename + " -C " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    # gzip
    if prod_download_filename.endswith(".gz") or prod_download_filename.endswith(".GZ") or prod_download_filename.endswith(".tgz") or prod_download_filename.endswith(".TGZ"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("tar xzvf " + prod_download_filename + " -C " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    # t64.gz
    if prod_download_filename.endswith(".t64.gz") or prod_download_filename.endswith(".T64.GZ"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("cd " + datadir + "dtrx -r " + prod_download_filename)
        if ret == 1:
            print("\tExtracting file failed!")
            
    # arc
    if prod_download_filename.endswith(".arc") or prod_download_filename.endswith(".ARC"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("arc x " + prod_download_filename + " " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    # arj
    if prod_download_filename.endswith(".arj") or prod_download_filename.endswith(".ARJ"):
        print("\tExtracting:", prod_download_filename)
        print("\tTo:", datadir)
        ret = os.system("arj x " + prod_download_filename + " " + datadir)
        if ret == 1:
            print("\tExtracting file failed!")
            
    open(datadir + "/.FILES_DOWNLOADED", 'a').close()

runner.setup(showetdir, datadir, prod_platform)
runner.run()
