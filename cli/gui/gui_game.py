"""
Snake Water Gun Game - Tkinter GUI with Pygame Sound
Robust audio handling with absolute paths and proper sound management
"""

import tkinter as tk
import random
import pygame
from pathlib import Path
import sys

# ============================================================================
# 🔊 AUDIO INITIALIZATION & PATH RESOLUTION
# ============================================================================

# Get the absolute directory of this script (works from any location)
SCRIPT_DIR = Path(__file__).resolve().parent
print("=" * 70)
print("🔍 AUDIO SYSTEM INITIALIZATION")
print("=" * 70)
print(f"\n📍 Script location: {SCRIPT_DIR}")

# Calculate assets directory path (navigate up 2 levels: gui → cli → project root)
ASSETS_DIR = SCRIPT_DIR.parent.parent / "assets"
print(f"📁 Assets directory: {ASSETS_DIR}")
print(f"   Exists: {'✅ YES' if ASSETS_DIR.exists() else '❌ NO'}")

# Define all sound files with their required extensions
SOUND_CONFIGS = {
    "click": {
        "file": "button_click.wav",
        "path": ASSETS_DIR / "button_click.wav",
        "required": True,
    },
    "victory": {
        "file": "victory.wav",
        "path": ASSETS_DIR / "victory.wav",
        "required": True,
    },
    "defeat": {
        "file": "defeat.wav",
        "path": ASSETS_DIR / "defeat.wav",
        "required": True,
    },
    "tie": {
        "file": "draw.wav",
        "path": ASSETS_DIR / "draw.wav",
        "required": True,
    },
}

# Initialize pygame mixer BEFORE loading sounds
# Parameters: frequency, size, channels, buffer
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    print(f"\n✅ Pygame mixer initialized")
    print(f"   Frequency: {pygame.mixer.get_init()[0]} Hz")
    print(f"   Channels: {pygame.mixer.get_init()[2]}")
except Exception as e:
    print(f"\n❌ Failed to initialize mixer: {e}")
    pygame.mixer.init()  # Fallback to defaults

# Dictionary to store loaded sounds (prevents reloading)
SOUNDS = {}

# Load all sound files with comprehensive error handling
print(f"\n📋 Loading sound files:")
for sound_key, config in SOUND_CONFIGS.items():
    sound_path = config["path"]
    sound_name = config["file"]
    
    # Check if file exists
    if not sound_path.exists():
        error_msg = f"   ❌ {sound_name:<25} NOT FOUND"
        print(error_msg)
        if config["required"]:
            print(f"      Expected at: {sound_path}")
        SOUNDS[sound_key] = None
        continue
    
    # Check file extension
    if sound_path.suffix.lower() not in [".wav", ".ogg", ".flac"]:
        print(f"   ⚠️  {sound_name:<25} (Unsupported format: {sound_path.suffix})")
        SOUNDS[sound_key] = None
        continue
    
    # Try to load the sound
    try:
        sound = pygame.mixer.Sound(str(sound_path))
        SOUNDS[sound_key] = sound
        file_size = sound_path.stat().st_size / 1024  # Size in KB
        duration = sound.get_length()  # Duration in seconds
        print(f"   ✅ {sound_name:<25} ({file_size:>7.1f} KB, {duration:>5.2f}s)")
    except pygame.error as e:
        print(f"   ❌ {sound_name:<25} (Load error: {str(e)[:40]}...)")
        SOUNDS[sound_key] = None
    except Exception as e:
        print(f"   ⚠️  {sound_name:<25} (Unexpected error: {type(e).__name__})")
        SOUNDS[sound_key] = None

# Verify at least one sound is loaded
loaded_count = sum(1 for s in SOUNDS.values() if s is not None)
total_count = len(SOUNDS)
print(f"\n📊 Status: {loaded_count}/{total_count} sounds loaded")

if loaded_count == 0:
    print("   ⚠️  NO SOUNDS LOADED - Game will run without audio")

print("=" * 70 + "\n")

# ============================================================================
# 🎮 GAME LOGIC & SOUND PLAYBACK
# ============================================================================

# Score tracking
user_score = 0
computer_score = 0

# Track current playing sounds to prevent overlaps
CURRENT_SOUND_CHANNEL = None


def stop_all_sounds():
    """
    Stop all currently playing sounds to prevent overlaps/interference
    """
    pygame.mixer.stop()


def play_sound(sound_key, description=""):
    """
    Play a sound safely with overlap prevention
    
    Args:
        sound_key: Key from SOUNDS dict (e.g., 'victory', 'defeat')
        description: Optional description of why sound is playing
    
    Returns:
        True if sound was played, False otherwise
    """
    # Check if sound exists and is loaded
    if sound_key not in SOUNDS:
        print(f"  ⚠️  Unknown sound key: {sound_key}")
        return False
    
    sound = SOUNDS[sound_key]
    
    if sound is None:
        print(f"  ℹ️  Sound not available: {sound_key} (file missing or corrupted)")
        return False
    
    try:
        # Stop any currently playing game sounds to prevent overlaps
        # (This prevents the "wrong sound" issue)
        stop_all_sounds()
        
        # Play the new sound
        sound.play()
        print(f"  🔊 Playing: {sound_key} {description}")
        return True
    except Exception as e:
        print(f"  ❌ Error playing {sound_key}: {e}")
        return False


def play(user_choice):
    """
    Main game logic - processes user choice and determines winner
    
    Args:
        user_choice: 'snake', 'water', or 'gun'
    """
    global user_score, computer_score
    
    print(f"\n🎮 GAME ROUND")
    print(f"  User chose: {user_choice}")
    
    # Play button click sound
    play_sound("click", "(button pressed)")
    
    # Get computer's random choice
    comp = random.choice(["snake", "water", "gun"])
    print(f"  Computer chose: {comp}")
    
    # Determine winner
    if user_choice == comp:
        result = "Tie!"
        result_color = "🟡"
        play_sound("tie", "(tie game)")
    
    elif (user_choice == "snake" and comp == "water") or \
         (user_choice == "water" and comp == "gun") or \
         (user_choice == "gun" and comp == "snake"):
        
        result = "You Win 🎉"
        result_color = "🟢"
        user_score += 1
        play_sound("victory", "(you won!)")
    
    else:
        result = "Computer Wins 🤖"
        result_color = "🔴"
        computer_score += 1
        play_sound("defeat", "(computer won)")
    
    print(f"  {result_color} Result: {result}")
    print(f"  Score: You {user_score} vs Computer {computer_score}")
    
    # Update UI labels
    result_label.config(
        text=f"You: {user_choice.upper()} | Computer: {comp.upper()}\n{result}"
    )
    score_label.config(
        text=f"Score → You: {user_score} | Computer: {computer_score}"
    )


# ============================================================================
# 🖥️ GUI SETUP
# ============================================================================

root = tk.Tk()
root.title("Snake Water Gun Game")
root.geometry("400x300")

# Title
title_label = tk.Label(
    root,
    text="🐍💧🔫 Snake Water Gun 🐍💧🔫",
    font=("Arial", 16, "bold"),
    fg="darkblue"
)
title_label.pack(pady=10)

# Instructions
instructions_label = tk.Label(
    root,
    text="Click a button to play:",
    font=("Arial", 12),
)
instructions_label.pack(pady=5)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buttons for choices
snake_btn = tk.Button(
    button_frame,
    text="🐍 Snake",
    command=lambda: play("snake"),
    font=("Arial", 11, "bold"),
    width=12,
    height=2,
    bg="#90EE90",
    activebackground="#7CCD7C"
)
snake_btn.pack(side="left", padx=5)

water_btn = tk.Button(
    button_frame,
    text="💧 Water",
    command=lambda: play("water"),
    font=("Arial", 11, "bold"),
    width=12,
    height=2,
    bg="#87CEEB",
    activebackground="#6BB6CD"
)
water_btn.pack(side="left", padx=5)

gun_btn = tk.Button(
    button_frame,
    text="🔫 Gun",
    command=lambda: play("gun"),
    font=("Arial", 11, "bold"),
    width=12,
    height=2,
    bg="#FFB6C1",
    activebackground="#FFA0B8"
)
gun_btn.pack(side="left", padx=5)

# Result display
result_label = tk.Label(
    root,
    text="Make your first move!",
    font=("Arial", 12),
    fg="darkgreen",
    height=3
)
result_label.pack(pady=10)

# Score display
score_label = tk.Label(
    root,
    text="Score → You: 0 | Computer: 0",
    font=("Arial", 11, "bold"),
    fg="darkblue"
)
score_label.pack(pady=10)

# Reset button
def reset_game():
    """Reset the game score and UI"""
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    score_label.config(text="Score → You: 0 | Computer: 0")
    result_label.config(text="Make your first move!")
    print("\n🔄 GAME RESET")


reset_btn = tk.Button(
    root,
    text="Reset Game",
    command=reset_game,
    font=("Arial", 10),
    bg="#FFD700",
    activebackground="#FFC700"
)
reset_btn.pack(pady=5)

# Audio status indicator
audio_status = "✅ Audio ON" if loaded_count > 0 else "⚠️ Audio OFF (no sounds loaded)"
status_label = tk.Label(
    root,
    text=audio_status,
    font=("Arial", 9),
    fg="gray"
)
status_label.pack(side="bottom", pady=5)

# Start the game
print("\n✨ Game started! Click a button to play.\n")
root.mainloop()

# Cleanup when window closes
pygame.mixer.stop()
pygame.mixer.quit()
print("\n👋 Game closed. Audio system shutdown.")