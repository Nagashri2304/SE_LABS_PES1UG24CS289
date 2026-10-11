import pygame
from .round import Round
from .sounds import SoundManager

# Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (75, 80, 88)
GREEN = (40, 185, 95)
BLUE = (45, 95, 180)
RED = (215, 55, 55)
DARK_BG = (24, 28, 36)
CARD_BG = (36, 42, 54)
ACCENT_YELLOW = (255, 205, 60)
ACCENT_CYAN = (70, 200, 240)
BTN_BG = (48, 56, 72)
BTN_HOVER = (68, 78, 102)
BTN_BORDER = (100, 115, 145)

DIFFICULTIES = {
    "Easy": {"min_wait_ms": 2000, "max_wait_ms": 4000, "rounds_total": 3, "desc": "2-4s wait | 3 rounds"},
    "Medium": {"min_wait_ms": 1000, "max_wait_ms": 3000, "rounds_total": 5, "desc": "1-3s wait | 5 rounds"},
    "Hard": {"min_wait_ms": 500, "max_wait_ms": 2000, "rounds_total": 7, "desc": "0.5-2s wait | 7 rounds"},
}

class GameEngine:
    def __init__(self, width, height, difficulty="Medium"):
        self.width = width
        self.height = height

        # Audio Manager
        self.sound_manager = SoundManager()

        # Fonts
        self.font = pygame.font.SysFont("Arial", 22)
        self.font_bold = pygame.font.SysFont("Arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.big_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)

        self.should_quit = False
        self.reset_game(difficulty=difficulty)

    def reset_game(self, difficulty="Medium"):
        """Resets the game session with the chosen difficulty settings."""
        self.difficulty = difficulty
        cfg = DIFFICULTIES.get(difficulty, DIFFICULTIES["Medium"])
        self.rounds_total = cfg["rounds_total"]
        self.min_wait_ms = cfg["min_wait_ms"]
        self.max_wait_ms = cfg["max_wait_ms"]

        self.round_history = []   # list of dicts: {'round': int, 'time': int or None, 'false_start': bool}
        self.reaction_times = []  # valid reaction times only
        self.round_index = 0

        self.round = Round(self.min_wait_ms, self.max_wait_ms)
        self.result_shown_at = None
        self.result_pause_ms = 1000

        self.game_over = False
        self.game_over_sound_played = False
        self.hovered_btn = None

    def handle_event(self, event):
        if self.game_over:
            self._handle_game_over_event(event)
            return

        is_click = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        is_space = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE

        if (is_click or is_space) and self.round.state in ("waiting", "go"):
            if self.round.state == "waiting":
                # False start triggered
                self.round.register_input(self.sound_manager)
                self.round_history.append({
                    "round": self.round_index + 1,
                    "time": None,
                    "false_start": True
                })
                self.result_shown_at = pygame.time.get_ticks()

            elif self.round.state == "go":
                # Valid reaction time
                reaction_ms = self.round.register_input(self.sound_manager)
                self.reaction_times.append(reaction_ms)
                self.round_history.append({
                    "round": self.round_index + 1,
                    "time": reaction_ms,
                    "false_start": False
                })
                self.result_shown_at = pygame.time.get_ticks()

    def _handle_game_over_event(self, event):
        """Handles replay difficulty selection and exit commands on the Game Over screen."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_KP1):
                self.reset_game("Easy")
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.reset_game("Medium")
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.reset_game("Hard")
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.should_quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            buttons = self._get_replay_buttons()
            for key, rect, label in buttons:
                if rect.collidepoint(mouse_pos):
                    if key == "Exit":
                        self.should_quit = True
                    else:
                        self.reset_game(key)
                    break

    def _get_replay_buttons(self):
        """Returns the bounding rects and labels for interactive difficulty buttons."""
        btn_w, btn_h = 160, 48
        y_pos = 280
        buttons = [
            ("Easy", pygame.Rect(35, y_pos, btn_w, btn_h), "[1] Easy (3 Rnds)"),
            ("Medium", pygame.Rect(220, y_pos, btn_w, btn_h), "[2] Medium (5 Rnds)"),
            ("Hard", pygame.Rect(405, y_pos, btn_w, btn_h), "[3] Hard (7 Rnds)"),
            ("Exit", pygame.Rect(220, y_pos + 60, btn_w, 38), "[Q] Exit Game"),
        ]
        return buttons

    def handle_input(self, mouse_pos=None):
        """Tracks mouse position for button hover highlights."""
        if self.game_over:
            if mouse_pos is None:
                mouse_pos = pygame.mouse.get_pos()
            self.hovered_btn = None
            for key, rect, _ in self._get_replay_buttons():
                if rect.collidepoint(mouse_pos):
                    self.hovered_btn = key
                    break

    def update(self):
        if self.game_over:
            if not self.game_over_sound_played:
                self.sound_manager.play_game_over()
                self.game_over_sound_played = True
                print("Game Over! Reaction times (ms):", self.reaction_times)
                print(f"Average: {self.average_reaction_ms()} ms | Best: {self.best_reaction_ms()} ms")
            return

        self.round.update(self.sound_manager)

        if self.round.state in ("result", "false_start"):
            now = pygame.time.get_ticks()
            if now - self.result_shown_at >= self.result_pause_ms:
                self._start_next_round()

    def _start_next_round(self):
        self.round_index += 1
        if len(self.round_history) >= self.rounds_total:
            self.game_over = True
            return
        self.round = Round(self.min_wait_ms, self.max_wait_ms)

    def average_reaction_ms(self):
        if not self.reaction_times:
            return 0
        return round(sum(self.reaction_times) / len(self.reaction_times))

    def best_reaction_ms(self):
        if not self.reaction_times:
            return 0
        return min(self.reaction_times)

    def get_performance_rating(self):
        avg = self.average_reaction_ms()
        if not self.reaction_times:
            return "Too many false starts! Try again."
        if avg < 200:
            return "Lightning Reflexes! (Elite)"
        elif avg < 250:
            return "Pro Gamer Speed! (Excellent)"
        elif avg < 320:
            return "Good Reflexes! (Above Average)"
        else:
            return "Practice Needed! (Below Average)"

    def render(self, screen):
        if self.game_over:
            self._render_game_over(screen)
            return

        # Active gameplay rendering
        if self.round.state == "waiting":
            bg = GRAY
            main_msg = "Wait for green..."
            sub_msg = "Clicking now causes a FALSE START!"
        elif self.round.state == "go":
            bg = GREEN
            main_msg = "CLICK NOW!"
            sub_msg = "React as fast as possible!"
        elif self.round.state == "false_start":
            bg = RED
            main_msg = "TOO EARLY!"
            sub_msg = "False Start! Wait until the screen turns green."
        else:
            bg = BLUE
            main_msg = f"{self.round.reaction_ms} ms"
            sub_msg = "Good reaction! Preparing next round..."

        screen.fill(bg)

        # Main Central Message
        text_surf = self.big_font.render(main_msg, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 - 15))
        screen.blit(text_surf, text_rect)

        sub_surf = self.font.render(sub_msg, True, (240, 240, 240))
        sub_rect = sub_surf.get_rect(center=(self.width // 2, self.height // 2 + 35))
        screen.blit(sub_surf, sub_rect)

        # Header Info Bar
        round_display = min(self.round_index + 1, self.rounds_total)
        round_text = self.font_bold.render(
            f"Round {round_display}/{self.rounds_total} [{self.difficulty}]", True, WHITE
        )
        screen.blit(round_text, (15, 12))

        avg_str = f"Avg: {self.average_reaction_ms()} ms" if self.reaction_times else "Avg: -- ms"
        avg_text = self.font_bold.render(avg_str, True, WHITE)
        screen.blit(avg_text, (self.width - avg_text.get_width() - 15, 12))

    def _render_game_over(self, screen):
        """Renders the comprehensive results screen with performance analytics and replay menu."""
        screen.fill(DARK_BG)

        # Header Title
        title_surf = self.title_font.render("SESSION COMPLETE", True, ACCENT_YELLOW)
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        # Stats Card
        card_rect = pygame.Rect(30, 62, self.width - 60, 110)
        pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=10)
        pygame.draw.rect(screen, BTN_BORDER, card_rect, width=1, border_radius=10)

        avg = self.average_reaction_ms()
        best = self.best_reaction_ms()
        false_starts = sum(1 for r in self.round_history if r.get("false_start"))

        avg_text = f"Average: {avg} ms" if self.reaction_times else "Average: N/A"
        best_text = f"Best: {best} ms" if self.reaction_times else "Best: N/A"
        fs_text = f"False Starts: {false_starts}"

        stat_s1 = self.font_bold.render(avg_text, True, ACCENT_CYAN)
        stat_s2 = self.font_bold.render(best_text, True, GREEN)
        stat_s3 = self.font_bold.render(fs_text, True, RED if false_starts > 0 else WHITE)

        screen.blit(stat_s1, (50, 75))
        screen.blit(stat_s2, (230, 75))
        screen.blit(stat_s3, (410, 75))

        # Rating banner
        rating = self.get_performance_rating()
        rating_surf = self.font.render(f"Rating: {rating}", True, WHITE)
        screen.blit(rating_surf, (50, 108))

        # Rounds breakdown row
        history_title = self.small_font.render("Rounds:", True, (180, 185, 200))
        screen.blit(history_title, (50, 142))

        x_offset = 115
        for item in self.round_history:
            if item["false_start"]:
                t_str = f"R{item['round']}: FS"
                t_col = (255, 110, 110)
            else:
                t_str = f"R{item['round']}: {item['time']}ms"
                t_col = (180, 230, 255)
            r_surf = self.small_font.render(t_str, True, t_col)
            screen.blit(r_surf, (x_offset, 142))
            x_offset += r_surf.get_width() + 12

        # Replay prompt
        prompt_surf = self.font_bold.render("Play Again - Choose Difficulty:", True, WHITE)
        screen.blit(prompt_surf, (self.width // 2 - prompt_surf.get_width() // 2, 240))

        # Interactive Difficulty Buttons
        for key, rect, label in self._get_replay_buttons():
            is_hover = (self.hovered_btn == key)
            bg_col = BTN_HOVER if is_hover else BTN_BG
            border_col = ACCENT_YELLOW if is_hover else BTN_BORDER

            pygame.draw.rect(screen, bg_col, rect, border_radius=8)
            pygame.draw.rect(screen, border_col, rect, width=2 if is_hover else 1, border_radius=8)

            txt_col = ACCENT_YELLOW if is_hover else WHITE
            btn_font = self.font_bold if is_hover else self.font
            btn_text = btn_font.render(label, True, txt_col)
            btn_rect = btn_text.get_rect(center=rect.center)
            screen.blit(btn_text, btn_rect)
