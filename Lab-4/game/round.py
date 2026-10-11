import random
import pygame

class Round:
    def __init__(self, min_wait_ms=1000, max_wait_ms=3000):
        self.wait_delay_ms = random.randint(min_wait_ms, max_wait_ms)
        self.state = "waiting"  # "waiting" -> "go" -> "result" | "false_start"
        self.start_time = pygame.time.get_ticks()
        self.go_time = None
        self.reaction_ms = None
        self.is_false_start = False

    def update(self, sound_manager=None):
        if self.state == "waiting":
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.wait_delay_ms:
                self.state = "go"
                self.go_time = now
                if sound_manager:
                    sound_manager.play_go()

    def register_input(self, sound_manager=None):
        """
        Handles player input:
        1. If screen is still in 'waiting' phase: flags as a FALSE START.
        2. If screen is in 'go' phase: records reaction time accurately measured
           from the exact moment 'go' occurred (self.go_time).
        """
        now = pygame.time.get_ticks()

        if self.state == "waiting":
            # Clicked too early before the green cue
            self.state = "false_start"
            self.is_false_start = True
            self.reaction_ms = None
            if sound_manager:
                sound_manager.play_false_start()
            return None

        elif self.state == "go":
            # Genuine reaction after the green cue
            # Elapsed time is accurately measured from self.go_time
            self.reaction_ms = max(1, now - self.go_time)
            self.state = "result"
            self.is_false_start = False
            return self.reaction_ms

        return self.reaction_ms
