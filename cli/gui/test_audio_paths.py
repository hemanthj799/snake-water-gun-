"""
Test script to verify path resolution without launching the GUI
Shows the debugging output for sound file paths
"""

import sys
from pathlib import Path

# Simulate the path resolution code
print("=" * 60)
print("🔍 SOUND FILE PATH RESOLUTION TEST")
print("=" * 60)

# Get this script's directory
SCRIPT_DIR = Path(__file__).resolve().parent
print(f"\n✓ Script location: {SCRIPT_DIR}")
print(f"  (__file__ = {Path(__file__).resolve()})")

# Navigate to project root
ASSETS_DIR = SCRIPT_DIR.parent.parent / "assets"
print(f"\n✓ Assets directory:")
print(f"  SCRIPT_DIR.parent = {SCRIPT_DIR.parent}")
print(f"  ASSETS_DIR = {ASSETS_DIR}")

# Check if assets directory exists
print(f"\n✓ Checking directories:")
print(f"  Assets folder exists: {ASSETS_DIR.exists()}")

# List all sound files
SOUND_FILES = {
    "victory.wav": ASSETS_DIR / "victory.wav",
    "defeat.wav": ASSETS_DIR / "defeat.wav",
    "button_click.wav": ASSETS_DIR / "button_click.wav",
    "draw.wav": ASSETS_DIR / "draw.wav",
}

print(f"\n✓ Sound file status:")
for name, path in SOUND_FILES.items():
    exists = "✅" if path.exists() else "❌"
    print(f"  {exists} {name:<20} → {path}")

# Try loading with pygame
try:
    import pygame
    pygame.mixer.init()
    
    print(f"\n✓ Pygame mixer initialized")
    
    loaded_count = 0
    for name, path in SOUND_FILES.items():
        try:
            if path.exists():
                sound = pygame.mixer.Sound(str(path))
                print(f"  ✅ Loaded: {name}")
                loaded_count += 1
            else:
                print(f"  ❌ Not found: {name}")
        except pygame.error as e:
            print(f"  ⚠️  Error loading {name}: {e}")
    
    print(f"\n✅ Successfully loaded {loaded_count}/4 sound files")
    
except ImportError:
    print("\n⚠️  pygame not installed. Install with: pip install pygame")

print("\n" + "=" * 60)
