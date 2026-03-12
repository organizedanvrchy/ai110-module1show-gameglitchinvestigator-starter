# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose

This is a number guessing game built with Streamlit where the player tries to guess a randomly chosen secret number within a limited number of attempts. The difficulty setting controls both the range of possible numbers (Easy: 1–20, Normal: 1–50, Hard: 1–100) and the number of attempts allowed (Easy: 8, Normal: 6, Hard: 5). After each guess, the player receives a hint telling them to go higher or lower, and a score is tracked based on how many attempts it took to find the answer. A developer debug dropdown is also available showing the secret number, attempt count, score, and guess history for testing purposes.

### Bugs Found

- **Reversed hint messages** <br>
When a guess was too high, the game told the player to go `HIGHER`, and when it was too low, it said to go `LOWER`. The outcome labels (`"Too High"`, `"Too Low"`) were correct, but the hint messages paired with them were completely swapped in `check_guess()`.

- **Secret number corruption on even attempts** <br>
Every other guess, the code intentionally cast the secret number from an Integer to a String before passing it into `check_guess()`. Since Python compares strings lexicographically rather than numerically, this caused incorrect hint results — for example, `"9"` would appear greater than `"50"` because `"9"` comes after `"5"` alphabetically.

- **New game button not fully resetting** <br>
Clicking New Game randomized the secret number and reset the attempt counter, but it did not reset the score, clear the guess history, or reset the game status. This meant a player who won or lost would see their old score and history carry over into the next game.

- **Attempts initializing to 1 instead of 0** <br>
`st.session_state.attempts` was initialized to `1` at the start of a new session, causing the attempts remaining counter to display one fewer attempt than intended from the very first guess.

- **Difficulty range not used in New Game** <br>
The New Game button was hardcoding `random.randint(1, 100)` regardless of the selected difficulty, instead of using the `low` and `high` values returned by `get_range_for_difficulty()`.

### Fixes Applied

- **Reversed hints**: Corrected the return values in `check_guess()` in `logic_utils.py` so that a guess above the secret returns `"📉 Go LOWER!"` and a guess below returns `"📈 Go HIGHER!"`.

- **String corruption**: Removed the conditional `str()` cast and replaced it with `secret = st.session_state.secret`, ensuring the secret is always compared as an Integer.

- **New game reset**: Added `st.session_state.score = 0`, `st.session_state.history = []`, and `st.session_state.status = "playing"` to the New Game handler so all state is fully cleared.

- **Attempts initialization**: Changed `st.session_state.attempts = 1` to `st.session_state.attempts = 0` so the counter starts correctly.

- **Difficulty range**: Updated the New Game handler to use `random.randint(low, high)` based on the selected difficulty, and updated `get_range_for_difficulty()` so the ranges scale correctly per difficulty level.

- **Refactored logic**: Moved `get_range_for_difficulty()`, `parse_guess()`, `check_guess()`, and `update_score()` out of `app.py` and into `logic_utils.py`, making the functions independently testable with pytest.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
