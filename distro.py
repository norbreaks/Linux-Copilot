import os

DISTRO_MAP = {
    "arch": "pacman -S",
    "manjaro": "pacman -S",
    "ubuntu": "apt install",
    "debian": "apt install",
    "fedora": "dnf install",
    "opensuse": "zypper install",
    "void": "xbps-install",
}

def detect_distro():
    """Reads /etc/os-release to detect the underlying Linux distribution. Fits gracefully if run on Windows for dev/testing."""
    if os.name == 'nt':
        return "windows-wsl" # Graceful fallback for Windows testing
        
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"').lower()
    except FileNotFoundError:
        pass
    return "unknown"

def get_package_manager():
    """Returns the correct package manager install command based on distro."""
    distro = detect_distro()
    for key, cmd in DISTRO_MAP.items():
        if key in distro:
            return cmd
    return "apt install"  # fallback
