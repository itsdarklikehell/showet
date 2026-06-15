# Android Platform Support

## Supported Emulators

```python
emulators = ['android-emulator', 'anbox', 'qemu']
```

## Supported File Extensions

```python
extensions = ['apk', 'aab', 'xapk']
```

## Installation

Android demos require an Android emulator. Options:

### Anbox (Recommended for Linux)
```bash
# Ubuntu/Debian
sudo snap install anbox

# Requires kernel modules: ashmem, binder
sudo modprobe ashmem_linux
sudo modprobe binder_linux
```

### Android SDK Emulator
```bash
# Install Android Studio or SDK tools
# Create an AVD (Android Virtual Device)
avdmanager create avd -n showet_demo -k "system-images;android-30;google_apis;x86_64"
```

### QEMU
```bash
sudo apt install qemu-kvm qemu-system-x86
# Requires Android x86 ISO
```

## Usage

```bash
showet --platforms | grep -i android
```

## Notes

- No official libretro core exists for Android yet
- Anbox provides the smoothest Linux experience
- APK package name extraction requires `aapt` from Android SDK for proper handling
- Demos may require touchscreen or specific Android features