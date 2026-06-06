import os
import shutil


SDK_VENDOR_DIRS = {
    "ocean": os.path.join("OceanSpectrometer", "Oceandirect", "lib"),
    "cni": os.path.join("CNILaserSpectrometer", "SDK"),
    "avantes": os.path.join("AvanterSpectrometer", "SDK"),
}


def get_sdk_root():
    base_dir = os.environ.get("PYSPECTRACE_SDK_DIR")
    if not base_dir:
        if os.name == "nt":
            base_dir = os.path.join(
                os.environ.get("APPDATA", os.path.expanduser("~")),
                "PySpectrace",
                "sdk",
            )
        else:
            base_dir = os.path.join(os.path.expanduser("~"), ".pyspectrace", "sdk")
    return os.path.abspath(base_dir)


def get_vendor_sdk_dir(vendor):
    return os.path.join(get_sdk_root(), SDK_VENDOR_DIRS[vendor])


def get_package_sdk_dir(vendor, package_base_dir):
    return os.path.join(package_base_dir, SDK_VENDOR_DIRS[vendor])


def get_sdk_file(vendor, filename, package_base_dir):
    user_sdk_dir = get_vendor_sdk_dir(vendor)
    user_sdk_file = os.path.join(user_sdk_dir, filename)
    if os.path.exists(user_sdk_file):
        return user_sdk_file

    if os.path.isdir(user_sdk_dir):
        for root, _, files in os.walk(user_sdk_dir):
            if filename in files:
                return os.path.join(root, filename)

    return os.path.join(get_package_sdk_dir(vendor, package_base_dir), filename)


def install_sdk_files(vendor, file_paths):
    target_dir = get_vendor_sdk_dir(vendor)
    os.makedirs(target_dir, exist_ok=True)

    copied = []
    for file_path in file_paths:
        if not file_path or not os.path.isfile(file_path):
            continue
        destination = os.path.join(target_dir, os.path.basename(file_path))
        shutil.copy2(file_path, destination)
        copied.append(destination)
    return copied

