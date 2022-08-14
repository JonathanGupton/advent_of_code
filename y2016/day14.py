import _md5
from collections import defaultdict, deque
from typing import Optional, Union

LETTER = str
INDEX = int


def find_runs(hash) -> dict[int, Optional[Union[int, list[LETTER]]]]:  # {3: ["a"], 5: ["c"]}
    runs = {3: None, 5: []}
    triple_found = False
    i = 0
    hash_len = len(hash)
    while i < hash_len:
        if i <= hash_len - 3 and all(char == hash[i] for char in hash[i:i+3]):
            if not triple_found:
                runs[3] = hash[i]
                triple_found = True
            if i <= hash_len - 5 and all(char == hash[i] for char in hash[i+3:i+5]):
                runs[5].append(hash[i])
        i += 1
    return runs


def part_a():
    # salt = "abc"
    salt = "zpqevtbw"
    current = 0
    candidate_keys: dict[LETTER, deque[INDEX]] = defaultdict(deque)
    found_keys = 0
    key_indexes: list[INDEX] = []

    while found_keys < 64:
        salted_password = salt + str(current)
        hashed_password = _md5.md5(salted_password.encode("ascii")).hexdigest()
        runs = find_runs(hashed_password)

        for letter in runs[5]:
            while candidate_keys[letter]:
                candidate_index = candidate_keys[letter].popleft()
                if current - candidate_index <= 1000:
                    found_keys += 1
                    key_indexes.append(candidate_index)

        if runs[3]:
            candidate_keys[runs[3]].append(current)
        current += 1
    print(key_indexes[63])


def part_b():
    # salt = "abc"
    salt = "zpqevtbw"
    current = 0
    candidate_keys: dict[LETTER, deque[INDEX]] = defaultdict(deque)
    found_keys = 0
    key_indexes: list[INDEX] = []

    while found_keys < 64:
        salted_password = salt + str(current)
        hashed_password = _md5.md5(salted_password.encode("ascii")).hexdigest()
        for _ in range(2016):
            hashed_password = _md5.md5(hashed_password.encode("ascii")).hexdigest()
        runs = find_runs(hashed_password)
        for letter in runs[5]:
            while candidate_keys[letter]:
                candidate_index = candidate_keys[letter].popleft()
                if current - candidate_index <= 1000:
                    found_keys += 1
                    key_indexes.append(candidate_index)
        if runs[3]:
            candidate_keys[runs[3]].append(current)
        current += 1
    print(key_indexes[63])


part_a()
part_b()