from string import ascii_lowercase


VALID_LETTERS = [letter for letter in ascii_lowercase if letter not in "iol"]
PASSWORD_LEN = 8


def has_increasing_straight(password):
    for i, letter in enumerate(password[:-2]):
        letter_index = VALID_LETTERS.index(letter)
        if password[i : i + 3] == VALID_LETTERS[letter_index : letter_index + 3]:
            return True
    return False


def has_non_overlapping_pairs(password):
    n_pairs = 0
    i = 0
    while i < PASSWORD_LEN:
        if i + 1 < PASSWORD_LEN and password[i] == password[i + 1]:
            n_pairs += 1
            i += 2
        else:
            i += 1
        if n_pairs == 2:
            return True
    return False


def increment_password(password):
    for i, letter in reversed(list(enumerate(password))):
        if letter == "z":
            password[i] = "a"
            continue
        else:
            password[i] = VALID_LETTERS[VALID_LETTERS.index(letter) + 1]
            return password
    return password


def next_password(password):
    password = [*password]
    while True:
        password = increment_password(password)
        if has_non_overlapping_pairs(password) and has_increasing_straight(password):
            return "".join(password)


password1 = "vzbxkghb"
password2 = next_password(password1)
password3 = next_password(password2)
