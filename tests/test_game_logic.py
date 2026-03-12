from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# FIX: Tests targeting the reversed hint messages bug
# Previously, "Go HIGHER!" was shown when guess was too high (should be "Go LOWER!") and vice versa

def test_too_high_message_says_lower():
    # When guess is above the secret, the hint message must tell the player to go lower
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_message_says_higher():
    # When guess is below the secret, the hint message must tell the player to go higher
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_correct_guess_message():
    # Winning guess should return a congratulatory message
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

# FIX: Tests targeting the get_range_for_difficulty bug
# Ranges were not correctly scaled per difficulty

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

# FIX: Tests targeting the secret string corruption bug
# Previously, on even attempts the secret was cast to str, causing incorrect string comparisons

def test_check_guess_uses_numeric_comparison():
    # "9" > "50" in string comparison (lexicographic) but 9 < 50 numerically
    # This ensures check_guess always uses numeric comparison
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_check_guess_numeric_boundary():
    # 100 > 9 numerically but "100" < "9" lexicographically
    outcome, _ = check_guess(100, 9)
    assert outcome == "Too High"

# Tests for parse_guess

def test_parse_valid_integer():
    ok, value, _ = parse_guess("42")
    assert ok is True
    assert value == 42

def test_parse_empty_string():
    ok, _, err = parse_guess("")
    assert ok is False
    assert "guess" in err.lower()

def test_parse_none():
    ok, _, _ = parse_guess(None)
    assert ok is False

def test_parse_non_numeric():
    ok, _, err = parse_guess("abc")
    assert ok is False
    assert err is not None

def test_parse_decimal_truncates():
    # Decimal inputs should be truncated to int, not rejected
    ok, value, _ = parse_guess("7.9")
    assert ok is True
    assert value == 7
