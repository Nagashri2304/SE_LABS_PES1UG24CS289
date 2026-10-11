# Software Engineering (SE) Lab 4: Vibe Coding — Prompt Engineering History

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Section:** E (5th Semester)  
**Assigned Project:** Reaction Time Tester (`43_reaction-time-tester`)  
**Repo URL:** [https://github.com/SETAPESU26/43_reaction-time-tester](https://github.com/SETAPESU26/43_reaction-time-tester)  
**Date:** October 10, 2026  

---

## Executive Overview
The objective of Lab 4 is to use AI-assisted Vibe Coding and iterative prompt engineering to diagnose and fix broken code in an assigned game repository and add all features listed in the project README in under 3–4 prompt attempts.

---

## Multi-Turn Prompting Session & Iterative Engineering

### Task 1: Refine Input Timing Detection & False Start Handling
- **Objective:** Fix timer inflation and detect premature clicks during the waiting phase.
- **Prompt:**
  > "In the reaction-time-tester game, the timing logic in `game/round.py` is broken.
  > Currently, `reaction_ms` is measured from `self.start_time` (when the round began) instead of `self.go_time` (when the screen turned green). This inflates every genuine reaction time by the wait delay (1–3 seconds).
  > Furthermore, if the user clicks during the grey 'waiting' phase, it accepts it as a real reaction instead of flagging it as a false start.
  > Please fix `game/round.py` and update `game/game_engine.py` to:
  > 1. Accurately measure genuine reaction times from `self.go_time`.
  > 2. Detect premature clicks during the 'waiting' state, flag them as a FALSE START, set state to 'false_start', and display a red 'TOO EARLY! False Start!' screen without recording a distorted time into the running average."
- **LLM Solution:**
  1. Updated `Round.update()` to record `self.go_time = pygame.time.get_ticks()` when state changes from `waiting` to `go`.
  2. In `Round.register_input()`:
     - If `self.state == "waiting"`, transition to `false_start`, set `is_false_start = True`, trigger buzzer sound, and return `None`.
     - If `self.state == "go"`, compute `self.reaction_ms = max(1, now - self.go_time)`.
  3. In `GameEngine`: Added a distinct RED warning state (`"TOO EARLY!"`) and ensured running averages only include legitimate reaction times.
- **Verification:** Early clicks show a red false start screen; reactions after green cue record accurate reflex speeds (~210–240ms).

---

### Task 2: Implement Game Over Condition & Results Screen
- **Objective:** Replace terminal output with a comprehensive graphical results screen once all rounds are complete.
- **Prompt:**
  > "Currently, when all rounds finish, `game_engine.py` just sets `self.game_over = True` and prints the results to the console (stdout), leaving the Pygame window frozen on the last round's result.
  > Please implement a comprehensive graphical Game Over / Results screen in Pygame that displays:
  > 1. Session complete title banner.
  > 2. Statistical summary card showing Average Reaction Time, Best (Fastest) Reaction Time, and Total False Starts.
  > 3. A round-by-round breakdown list (e.g., R1: 230ms, R2: False Start, R3: 215ms).
  > 4. A reflex speed category rating (e.g., 'Lightning Reflexes!', 'Pro Gamer Speed!', 'Good Reflexes!').
  > 5. Gracefully waits for user interaction without closing or freezing."
- **LLM Solution:**
  1. Built `_render_game_over(screen)` in `GameEngine` with modern dark slate styling, rounded statistics card, and colored accent metrics.
  2. Implemented `best_reaction_ms()` and `get_performance_rating()` to classify human reaction speeds:
     - `< 200 ms`: Lightning Reflexes! (Elite)
     - `200 - 250 ms`: Pro Gamer Speed! (Excellent)
     - `250 - 320 ms`: Good Reflexes! (Above Average)
     - `> 320 ms`: Practice Needed! (Below Average)
  3. Rendered individual round pills showing each round's result and false start indicators.
- **Verification:** When all rounds complete, the results screen appears seamlessly with stats and rating.

---

### Task 3: Add Replay Option with Difficulty Selection
- **Objective:** Allow the user to play again by choosing a difficulty or exit cleanly.
- **Prompt:**
  > "On the Game Over screen, allow the player to play again by choosing a difficulty level or exit the game.
  > Add interactive difficulty options:
  > - Easy: 2–4 second wait time, 3 rounds
  > - Medium: 1–3 second wait time, 5 rounds
  > - Hard: 0.5–2 second wait time, 7 rounds
  > - Exit: Gracefully quit the game
  > Support both keyboard hotkeys (1, 2, 3, Q) and clickable on-screen buttons with mouse hover highlights.
  > Implement a clean `reset_game()` method that resets all counters and starts round 1 immediately upon selection."
- **LLM Solution:**
  1. Defined `DIFFICULTIES` configuration dictionary.
  2. Implemented `_get_replay_buttons()` and mouse tracking in `handle_input()` to dynamically highlight buttons on hover.
  3. Handled keyboard inputs (`1`, `2`, `3`, `Q`) and mouse clicks in `_handle_game_over_event()`.
  4. Added `should_quit` flag in `GameEngine` respected by the event loop in `main.py`.
- **Verification:** Hovering highlights buttons; pressing keys or clicking resets the game to the selected difficulty immediately.

---

### Task 4: Add Sound Feedback System
- **Objective:** Provide sound effects for the green "go" cue, false starts, and session completion.
- **Prompt:**
  > "Add audio sound feedback to the game for:
  > 1. 'Go' cue (when the screen turns green)
  > 2. False start (when the user clicks prematurely)
  > 3. Session ending / Game over (when all rounds finish)
  > Requirements: The sound system must be self-contained so it does not fail if external audio files are missing, and must handle headless or muted audio environments gracefully without crashing."
- **LLM Solution:**
  1. Created `game/sounds.py` containing a robust `SoundManager`.
  2. Procedurally synthesized 16-bit PCM WAV audio files using Python's standard `wave` and `math` modules:
     - `go.wav`: 880 Hz decaying sine chime (180ms).
     - `false_start.wav`: 160 Hz harsh dual-pulse square wave buzzer (280ms).
     - `game_over.wav`: 4-note ascending fanfare arpeggio (C5 -> E5 -> G5 -> C6, 550ms).
  3. Wrapped audio loading with graceful fallbacks if sound hardware is absent.
- **Verification:** Sounds play crisply at every event transition; fails gracefully without error if audio hardware is disabled.

---

## Deliverables Checklist
- [x] **Video Before Changes** (`videos/video_before.mp4`): 10 seconds showing false starts accepted and timing inflated by wait delay.
- [x] **Video After Changes** (`videos/video_after.mp4`): 12 seconds showing false start detection, true reaction timing, results UI, and replay difficulty selection.
- [x] **Updated Codebase**: `main.py`, `game/game_engine.py`, `game/round.py`, `game/sounds.py`, `requirements.txt`.
- [x] **Chat History Export**: Formatted DOCX and PDF documents (`chat_history/` and root).
