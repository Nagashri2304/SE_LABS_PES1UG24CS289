# Real-Time Reaction Time Tester — SE Lab 4: VibeCoding

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Section:** E (5th Semester)  
**Assigned Project:** Reaction Time Tester (`43_reaction-time-tester`)  
**Repo URL:** [https://github.com/SETAPESU26/43_reaction-time-tester](https://github.com/SETAPESU26/43_reaction-time-tester)  
**Submission Folder:** `D:\sem5\se\se_project_n\VibeCoding\Lab4_N`  

---

## Deliverables Summary

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Videos (Before & After)** | `videos/video_before.mp4`<br>`videos/video_after.mp4` | 10s gameplay before changes showing bugs; 12s gameplay after changes showing all features working. |
| **Updated Code** | `main.py`<br>`game/game_engine.py`<br>`game/round.py`<br>`game/sounds.py` | Complete fixed and enhanced code matching all tasks in the project README. |
| **Chat History Export** | `chat_history/VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.pdf`<br>`chat_history/VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.docx`<br>`chat_history/chat_history.md` | Complete multi-turn prompt logs, design rationale, code diffs, and verification steps exported as PDF and DOCX. |

---

## Tasks Completed

### Task 1: Refine Input Timing Detection & False Start Handling
- **Bug in Original Code:** Reaction time was computed as `now - self.start_time` (when the round began), inflating all reaction times by the random wait delay (1–3 seconds). Clicking during the grey wait phase was recorded as a normal reaction instead of a false start.
- **Resolution:**
  - `game/round.py`: Measures elapsed time strictly from `self.go_time` (when the screen turns green).
  - Clicking prematurely while `self.state == "waiting"` transitions the round to `"false_start"` with a red screen, buzzer sound, and is excluded from running average calculations.

### Task 2: Implement Game Over Condition & Results Screen
- **Bug in Original Code:** When all rounds finished, the engine only logged to `stdout` and stayed frozen on the last round's blue screen.
- **Resolution:**
  - `game/game_engine.py`: Added a graphical Game Over / Results screen displaying:
    - Session complete banner and reflex speed evaluation rating.
    - Summary card with Average Time, Best (Fastest) Time, and False Start Count.
    - Round-by-round breakdown pills (e.g. `R1: 230ms`, `R2: FS`, etc.).

### Task 3: Add Replay Option with Difficulty Selection
- **Feature Implemented:**
  - Allows players to choose from 3 difficulty levels on the Game Over screen:
    - **[1] Easy:** 2–4s wait delay, 3 rounds.
    - **[2] Medium:** 1–3s wait delay, 5 rounds.
    - **[3] Hard:** 0.5–2s wait delay, 7 rounds.
    - **[Q] Exit:** Gracefully exits the game.
  - Interactive clickable buttons with hover glow effects as well as keyboard shortcuts (`1`, `2`, `3`, `Q`).
  - Seamless reset and immediate launch of Round 1.

### Task 4: Add Sound Feedback
- **Feature Implemented:**
  - Created `game/sounds.py` with standalone procedural synthesis of standard 16-bit PCM WAV audio:
    - `go.wav`: 880 Hz decaying sine wave chime on green cue.
    - `false_start.wav`: 160 Hz dual-pulse square wave buzzer on premature clicks.
    - `game_over.wav`: 4-note ascending fanfare arpeggio (C5 -> E5 -> G5 -> C6) on results screen.
  - Graceful audio fallbacks for silent/headless systems.

---

## Folder Structure

```
Lab4_N/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies (pygame)
├── README.md                   # This project report & documentation
├── build_docs.py               # Document generator script
├── VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.docx
├── VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.pdf
│
├── game/
│   ├── __init__.py
│   ├── game_engine.py          # Complete engine with game over, replay, difficulty, sound
│   ├── round.py                # Accurate timing logic & false start detection
│   ├── sounds.py               # SoundManager & WAV synthesis
│   └── assets/
│       ├── go.wav
│       ├── false_start.wav
│       └── game_over.wav
│
├── videos/
│   ├── video_before.mp4        # 10s gameplay before changes (showing bugs)
│   └── video_after.mp4         # 12s gameplay after changes (showing all fixes)
│
├── chat_history/
│   ├── VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.docx
│   ├── VibeCoding_Lab4_PES1UG24CS289_Nagashri_R_Patil.pdf
│   └── chat_history.md
│
└── buggy_code_backup/          # Untouched original repo code for reference
    ├── main.py
    ├── requirements.txt
    ├── README.md
    └── game/
        ├── game_engine.py
        └── round.py
```

---

## How to Run

1. Open a terminal in this directory:
   ```bash
   cd D:\sem5\se\se_project_n\VibeCoding\Lab4_N
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. Controls:
   - Wait for the screen to turn green, then **Click** or press **SPACE**.
   - On the results screen, click the difficulty buttons or press `1`, `2`, `3` to replay, or `Q` to quit.
