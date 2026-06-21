"""Platform modules loader for Showet."""

import importlib
from pathlib import Path
from typing import Any


def load_all_platforms() -> list[Any]:
    """Load all Platform_*.py modules from the project root."""
    project_root = Path(__file__).parent.parent
    runners = []
    
    module_names = [
        "Platform_Alambik_Alambik",
        "Platform_Amstrad_Cpcplus",
        "Platform_Android_Android",
        "Platform_Apple_AppleI",
        "Platform_Apple_AppleII",
        "Platform_Apple_AppleIIGS",
        "Platform_Arcade_Arcade",
        "Platform_Archimedes_Acorn",
        "Platform_Atari_2600",
        "Platform_Atari_5200",
        "Platform_Atari_7800",
        "Platform_Atari_Jaguar",
        "Platform_Atari_Lynx",
        "Platform_Atari_ST",
        "Platform_Atari_STe",
        "Platform_Atari_STETTFalcon",
        "Platform_Atari_xlxe",
        "Platform_Bandai_Wonderswan",
        "Platform_Commodore_64",
        "Platform_Commodore_128",
        "Platform_Commodore_Amiga",
        "Platform_Commodore_Amiga_AGA",
        "Platform_Commodore_CBMII",
        "Platform_Commodore_Pet",
        "Platform_Commodore_Plus4",
        "Platform_Commodore_Vic20",
        "Platform_Elektronika_Pdp11",
        "Platform_Enterprise_Ep128",
        "Platform_Fairchild_Channelf",
        "Platform_FanCon_Pico8",
        "Platform_Flash_Ruffle",
        "Platform_Gamepark_2X",
        "Platform_Gamepark_32",
        "Platform_GCE_Vectrex",
        "Platform_Java_Java",
        "Platform_Linux_Linux",
        "Platform_Magnavox_Odyssey",
        "Platform_Mattel_Intellivision",
        "Platform_Microsoft_Msdos",
        "Platform_Microsoft_Msx",
        "Platform_Microsoft_Windows",
        "Platform_Microsoft_Xbox",
        "Platform_Nec_Pc98",
        "Platform_Nec_Pc8000",
        "Platform_Nec_Pc8800",
        "Platform_Nec_Pcengine",
        "Platform_Nec_Pcfx",
        "Platform_Nec_Supergrafx",
        "Platform_Nintendo_3DS",
        "Platform_Nintendo_Famicom",
        "Platform_Nintendo_FamicomDisksystem",
        "Platform_Nintendo_Gameboy",
        "Platform_Nintendo_GameboyAdvance",
        "Platform_Nintendo_GameboyColor",
        "Platform_Nintendo_GameCube",
        "Platform_Nintendo_N64",
        "Platform_Nintendo_Pokemini",
        "Platform_Nintendo_SuperFamicom",
        "Platform_Nintendo_VirtualBoy",
        "Platform_Nintendo_Wii",
        "Platform_Palm_PalmOS",
        "Platform_Panasonic_3do",
        "Platform_Phillips_Cdi",
        "Platform_Sega_32X",
        "Platform_Sega_Dreamcast",
        "Platform_Sega_GameGear",
        "Platform_Sega_Mastersystem",
        "Platform_Sega_Megadrive",
        "Platform_Sega_Saturn",
        "Platform_Sega_SG1000",
        "Platform_Sega_Stv",
        "Platform_Sega_Vmu",
        "Platform_Sharp_MZ",
        "Platform_Sinclair_Zx81",
        "Platform_Sinclair_Zxspectrum",
        "Platform_Spectrum_ZXEnhanced",
        "Platform_Snk_Neogeo",
        "Platform_Snk_NeogeoPocket",
        "Platform_Snk_NeogeoPocketColor",
        "Platform_Sony_Ps2",
        "Platform_Sony_Psp",
        "Platform_Sony_Psx",
        "Platform_SpectraVision_SpectraVideo",
        "Platform_Thomson_MOTO",
        "Platform_TI_8x",
        "Platform_Wild_Gamemusic",
        "Platform_Wild_VideoFFMPEG",
        "Platform_Wild_VideoMPV",
        "Platform_Tangerine_Oric",
        "Platform_WebAssembly_Web",
        "Platform_Raspberry_Pi",
    ]
    
    for mod_name in module_names:
        try:
            mod = importlib.import_module(mod_name)
            cls = getattr(mod, mod_name)
            runners.append(cls())
        except Exception:
            continue
    
    return runners


__all__ = ["load_all_platforms"]