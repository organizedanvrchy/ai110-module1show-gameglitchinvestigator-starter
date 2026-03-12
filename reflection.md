# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

Upon opening the game, I noticed a simple UI asking me to guess a number between 1 and 100 in about 8 attempts on the normal difficulty, along with a developer debug dropdown that shows the secret number.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

 When I attempted a guess, I was shown a hint telling me to go **'LOWER'** even though the secret number is actually higher than my number and vice versa, indicating that this logic is reversed. When I entered a guess, the history also updates incorrectly, and seems to use the previous input rather than the current input, most likely due to *attempts* being initialized to 1 instead of 0. Moreover, pressing the new game button randomizes the secret number and resets the number of attempts to 0, while it does not reset the score nor remove the history from the previous game.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code for this project. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI was able to find the bugs that I did and provided simple fixes for a few. For example, I asked Claude Code to explain the check_guess() function and whether the inequality logic was correct. Claude Code found the logical error and easily suggested flipping the return statements "📈 Go HIGHER!" when the guess is "Too Low" and "📉 Go LOWER!" when the guess is "Too High".

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The AI suggested that I fix the streamlit information displayed to the user to update correctly when changing difficulty, this is only changing the text displayed to the user so they know the range of numbers to make a guess. The AI notes that it is a *'Display-only inconsistency'* but missed the fact that the secret number was still always randomizing between 1 and 100 regardless of difficulty. This was simply verified by integrating the fix suggested by the AI, running the game, and clicking **'New Game'** a few times to notice that the secret number is outside of the expected range. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I decided that a bug was considered fixed when the game behaved as expected both visually in the browser and logically through automated tests. For UI-level bugs like the new game button not resetting the score and history, I verified the fix by manually running the app, playing through a game, and clicking New Game to confirm the score returned to 0 and the history cleared--using the debug menu. For logic-level bugs like the reversed hint messages, I confirmed the fix by running the pytest suite and checking that all assertions passed. Seeing a green test result alongside correct in-game behaviour gave me confidence that the fix was complete and didn't break anything else.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

One specific pytest test that was particularly revealing was *'test_too_high_message_says_lower'*, which called *'check_guess(75, 50)'* and asserted that the returned message contained the word **"LOWER"**. Before the fix, this test would have failed because the original code returned *"📈 Go HIGHER!"* when the guess was too high--the reversed-message bug. Running this test after the fix confirmed that *'check_guess'* now correctly returns *"📉 Go LOWER!"* when the guess exceeds the secret, giving me direct proof that the logic was repaired at the function level, not just appearing correct in the UI.

- Did AI help you design or understand any tests? How?

Claude Code helped me design the tests by explaining which parts of the code were worth unit testing and why. When I asked for tests targeting the bugs I had fixed, it pointed out that the existing three tests were comparing the full return value of *'check_guess'* against a plain string like **"Win"**, but *'check_guess'* actually returns a tuple *'(outcome, message)'*--meaning all three original tests were already broken and would have failed on the first run. Claude Code explained that this was a common mistake when a function's return type changes, and suggested unpacking the tuple with *'outcome, _ = check_guess(...)'* for tests that only care about the outcome, and *'outcome, message = check_guess(...)'* for tests that also verify the message content.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

From reading through the code, I noticed that there was something off about the secret number comparison to the user's guess. Although I was not entirely sure what the issue was at first, I used Claude Code to explain that portion of the code. Claude Code explained that there was some intentional corruption of the secret number on odd attempts by converting the secret number to a String instead of its actual data type of Integer.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time a user interacts with a Streamlit app; such as clicking a button, typing in a box, or changing a dropdown, the entire Python script reruns from the top. This means that any variable that is just assigned normally gets reset to its default value on every interaction, which is why the secret number was regenerating. Session state is Streamlit's way of letting you store values that survive across reruns, similar to how a webpage might remember a user's login between page refreshes. From my understanding, you simply store a value in *'st.session_state'* and check if it already exists before assigning it, so it only gets set once.

- What change did you make that finally gave the game a stable secret number?

I attempted removing the block of code that was intentionally casting the secret number to a String on even-numbered attempts before passing it into *'check_guess'*. Since Python compares strings lexicographically rather than numerically, a string secret would produce incorrect comparison results--for example, *'"9"'* would be considered greater than *'"50"'* because *'"9"'* comes after *'"5"'* alphabetically. The fix was replacing the conditional casting with a single line: *'secret = st.session_state.secret'*, so the secret is always passed as an Integer and compared correctly on every attempt. This made the game behave consistently on every guess, regardless of whether it was an odd or even attempt number.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

One habit I want to carry forward is writing unit tests alongside my code rather than as an afterthought. Working with pytest on this project showed me how useful it is to have tests that directly target specific functions, and I want to get more comfortable writing those tests manually without relying on AI to generate them for me. I noticed that when I understood what a test was actually checking--like asserting `"LOWER"` is in the hint message rather than just checking the outcome label--the tests became much more meaningful and caught real bugs. Going forward, I want to invest more time in learning pytest properly so I can build full test suites on my own.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time, I would try to rely less on the AI to directly write or edit code for me, and instead use it more as a resource for context, insights, or syntax information. I found that when the AI wrote code directly, I sometimes didn't fully understand what it changed or why, which made it harder to verify that the fix was actually correct. Asking the AI to explain what is wrong and what I should change--rather than just applying the change--would help me stay more in control of my own code. This project made it clear that understanding the fix matters just as much as getting the fix done.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project made me realize that AI-generated code is not something you can just accept and move on--it requires the same level of scrutiny as code written by anyone else, including myself. I now see AI as a tool to supplement my efficiency rather than something to fully rely on, and I am much more actively reading and understanding the code rather than letting the AI handle everything.
