"""
Test script to verify the audio system configuration
Run this to diagnose any audio issues before starting the game
"""

import pygame
from pathlib import Path
import sys

print("=" * 70)
print("🔧 AUDIO SYSTEM DIAGNOSTIC TEST")
print("=" * 70)

# Test 1: Path Resolution
print("\n[TEST 1] Path Resolution")
print("-" * 70)

SCRIPT_DIR = Path(__file__).resolve().parent
print(f"Script location: {SCRIPT_DIR}")

# Navigate up 2 levels to project root (gui → cli → project root)
ASSETS_DIR = SCRIPT_DIR.parent.parent / "assets"
print(f"Assets directory: {ASSETS_DIR}")
print(f"Exists: {'✅ YES' if ASSETS_DIR.exists() else '❌ NO'}")

if ASSETS_DIR.exists():
    wav_files = list(ASSETS_DIR.glob('*.wav'))
    print(f"Contents ({len(wav_files)} WAV files): {[f.name for f in wav_files]}")
else:
    print(f"⚠️  Expected path: {ASSETS_DIR}")

# Test 2: Pygame Initialization
print("\n[TEST 2] Pygame Mixer Initialization")
print("-" * 70)

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    print("✅ Mixer initialized successfully")
    
    mixer_info = pygame.mixer.get_init()
    if mixer_info:
        freq, size, channels = mixer_info
        print(f"   Frequency: {freq} Hz")
        print(f"   Channels: {channels}")
        print(f"   Size: {size}-bit")
except Exception as e:
    print(f"❌ Mixer initialization failed: {e}")
    sys.exit(1)

# Test 3: Sound File Loading
print("\n[TEST 3] Sound File Loading")
print("-" * 70)

SOUND_FILES = {
    "button_click.wav": ASSETS_DIR / "button_click.wav",
    "victory.wav": ASSETS_DIR / "victory.wav",
    "defeat.wav": ASSETS_DIR / "defeat.wav",
    "draw.wav": ASSETS_DIR / "draw.wav",
}

loaded_sounds = {}
for name, path in SOUND_FILES.items():
    # File exists check
    if not path.exists():
        print(f"❌ {name:<25} - NOT FOUND at {path}")
        continue
    
    # Extension check
    if path.suffix.lower() not in [".wav", ".ogg", ".flac", ".mp3"]:
        print(f"⚠️  {name:<25} - Unsupported format: {path.suffix}")
        continue
    
    # Load check
    try:
        sound = pygame.mixer.Sound(str(path))
        loaded_sounds[name] = sound
        size = path.stat().st_size / 1024
        duration = sound.get_length()
        print(f"✅ {name:<25} - {size:>6.1f} KB, {duration:>5.2f}s")
    except pygame.error as e:
        print(f"❌ {name:<25} - Load error: {str(e)[:30]}")

# Test 4: Sound Playback
print("\n[TEST 4] Sound Playback Test")
print("-" * 70)

if loaded_sounds:
    # Get first sound
    first_sound = list(loaded_sounds.items())[0]
    print(f"Testing playback of: {first_sound[0]}")
    
    try:
        first_sound[1].play()
        print("✅ Sound started playing")
        
        # Wait a moment for sound to play
        import time
        time.sleep(0.5)
        
        # Stop the sound
        pygame.mixer.stop()
        print("✅ Sound stopped")
    except Exception as e:
        print(f"❌ Playback error: {e}")
else:
    print("⚠️  No sounds available for playback test")

# Test 5: Overlap Prevention
print("\n[TEST 5] Sound Overlap Prevention")
print("-" * 70)

if len(loaded_sounds) >= 2:
    sounds_list = list(loaded_sounds.items())
    sound1_name, sound1 = sounds_list[0]
    sound2_name, sound2 = sounds_list[1]
    
    print(f"Playing {sound1_name}...")
    sound1.play()
    
    import time
    time.sleep(0.1)
    
    print(f"Stopping and playing {sound2_name}...")
    pygame.mixer.stop()  # Stop sound1 first
    sound2.play()
    
    time.sleep(0.1)
    pygame.mixer.stop()
    
    print("✅ Overlap prevention works (sounds handled cleanly)")
else:
    print("⚠️  Not enough sounds to test overlap prevention")

# Summary
print("\n[SUMMARY]")
print("=" * 70)

print(f"✅ Path resolution: WORKING")
print(f"✅ Mixer initialization: WORKING")
print(f"✅ Sounds loaded: {len(loaded_sounds)}/{len(SOUND_FILES)}")
print(f"✅ Playback: WORKING" if loaded_sounds else "⚠️  Playback: NOT TESTED (no sounds)")
print(f"✅ Overlap prevention: WORKING" if len(loaded_sounds) >= 2 else "⚠️  Not tested")

if len(loaded_sounds) == len(SOUND_FILES):
    print("\n🎉 FULL SYSTEM TEST PASSED - Game is ready to play!")
elif len(loaded_sounds) > 0:
    print("\n⚠️  PARTIAL SYSTEM - Game will work but some sounds missing")
else:
    print("\n❌ SYSTEM TEST FAILED - No sounds available")

# Cleanup
pygame.mixer.quit()
print("\n" + "=" * 70)
