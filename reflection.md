# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Upon opening the game, I noticed a simple UI asking me to guess a number between 1 and 100 in about 8 attempts on the normal difficulty, along with a developer debug dropdown that shows the secret number. When I attempt a guess at the number, I get a hint telling me to go **'LOWER'** even though the secret number is actually higher than my number and vice versa, indicating that this logic is reversed. When I entered a guess, the history also updates incorrectly, and seems to use the previous input rather than the current input, most likely due to *attempts* being initialized to 1 instead of 0. Moreover, pressing the new game button randomizes the secret number and resets the number of attempts to 0, while it does not reset the score nor remove the history from the previous game.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code for this project. 

The AI was able to find the bugs that I did and provided simple fixes for a few. For example, I asked Claude Code to explain the check_guess() function and whether the inequality logic was correct. Claude Code found the logical error and easily suggested flipping the return statements "📈 Go HIGHER!" when the guess is "Too Low" and "📉 Go LOWER!" when the guess is "Too High".

The AI suggested that I fix the streamlit information displayed to the user to update correctly when changing difficulty, this is only changing the text displayed to the user so they know the range of numbers to make a guess. The AI notes that it is a *'Display-only inconsistency'* but missed the fact that the secret number was still always randomizing between 1 and 100 regardless of difficulty. This was simply verified by integrating the fix suggested by the AI, running the game, and clicking **'New Game'** a few times to notice that the secret number is outside of the expected range. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
