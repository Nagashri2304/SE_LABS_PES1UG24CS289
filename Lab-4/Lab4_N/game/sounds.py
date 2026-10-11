import os
import wave
import math
import struct
import pygame

class SoundManager:
    """
    Manages sound effects for the Reaction Time Tester.
    Provides audio feedback for:
    - 'go' cue (screen turning green)
    - false start (clicking before green)
    - session ending (results/game over fanfare)
    """
    def __init__(self, assets_dir=None):
        if assets_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            assets_dir = os.path.join(base_dir, "assets")
        self.assets_dir = assets_dir
        os.makedirs(self.assets_dir, exist_ok=True)

        self.sounds = {}
        self.enabled = False

        self._ensure_asset_files()
        self._init_audio()

    def _ensure_asset_files(self):
        """Generates standard PCM WAV sound files if they do not exist."""
        sample_rate = 44100

        def write_wav(path, samples):
            if os.path.exists(path):
                return
            with wave.open(path, "w") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                for s in samples:
                    val = max(-32767, min(32767, int(s * 32767)))
                    wav.writeframes(struct.pack("<h", val))

        # 1. go.wav (880Hz chime)
        go_path = os.path.join(self.assets_dir, "go.wav")
        if not os.path.exists(go_path):
            samples_go = []
            dur_go = 0.18
            for i in range(int(sample_rate * dur_go)):
                t = i / sample_rate
                env = math.exp(-14 * t)
                sig = 0.7 * math.sin(2 * math.pi * 880 * t) + 0.3 * math.sin(2 * math.pi * 1760 * t)
                samples_go.append(sig * env)
            write_wav(go_path, samples_go)

        # 2. false_start.wav (160Hz harsh buzzer)
        buzz_path = os.path.join(self.assets_dir, "false_start.wav")
        if not os.path.exists(buzz_path):
            samples_buzz = []
            dur_buzz = 0.28
            for i in range(int(sample_rate * dur_buzz)):
                t = i / sample_rate
                env = 0.8 if (t < 0.11 or (0.15 < t < 0.26)) else 0.0
                sig = 0.7 if (math.sin(2 * math.pi * 160 * t) > 0) else -0.7
                samples_buzz.append(sig * env)
            write_wav(buzz_path, samples_buzz)

        # 3. game_over.wav (fanfare C5 -> E5 -> G5 -> C6)
        over_path = os.path.join(self.assets_dir, "game_over.wav")
        if not os.path.exists(over_path):
            notes = [(523.25, 0.10), (659.25, 0.10), (783.99, 0.10), (1046.50, 0.25)]
            samples_fanfare = []
            for freq, dur in notes:
                n_s = int(sample_rate * dur)
                for i in range(n_s):
                    t = i / sample_rate
                    env = math.exp(-4 * (i / n_s))
                    sig = 0.6 * math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(2 * math.pi * freq * 2 * t)
                    samples_fanfare.append(sig * env)
            write_wav(over_path, samples_fanfare)

    def _init_audio(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            go_file = os.path.join(self.assets_dir, "go.wav")
            buzz_file = os.path.join(self.assets_dir, "false_start.wav")
            over_file = os.path.join(self.assets_dir, "game_over.wav")

            if os.path.exists(go_file):
                self.sounds["go"] = pygame.mixer.Sound(go_file)
            if os.path.exists(buzz_file):
                self.sounds["false_start"] = pygame.mixer.Sound(buzz_file)
            if os.path.exists(over_file):
                self.sounds["game_over"] = pygame.mixer.Sound(over_file)
            self.enabled = True
        except Exception as e:
            # Graceful fallback if audio hardware is disabled or unavailable
            print(f"Warning: Audio device initialization failed ({e}). Running in silent mode.")
            self.enabled = False

    def play_go(self):
        if self.enabled and "go" in self.sounds:
            self.sounds["go"].play()

    def play_false_start(self):
        if self.enabled and "false_start" in self.sounds:
            self.sounds["false_start"].play()

    def play_game_over(self):
        if self.enabled and "game_over" in self.sounds:
            self.sounds["game_over"].play()
