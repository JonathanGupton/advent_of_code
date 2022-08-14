from typing import Optional, Union
import hashlib

def part_a():
    found = []
    base = "reyedfim"
    salt = 0
    while len(found) < 8:
        salted_password = base + str(salt)
        result = hashlib.md5(salted_password.encode("ascii")).hexdigest()
        if result[:5] == "00000":
            found.append(result[5])
        salt += 1
    password = "".join(found)
    print(password)


def part_b():
    found: list[Optional[Union[str, int]]] = [None] * 8
    base = "reyedfim"
    salt = 0
    while not all(found):
        salted_password = base + str(salt)
        result = hashlib.md5(salted_password.encode("ascii")).hexdigest()
        if result[:5] == "00000":
            print(f"Trying hash {result}")
            try:
                position = int(result[5])
                if position <= 7 and found[position] is None:
                    found[position] = result[6]
                    temp_pass = []
                    for character in found:
                        if character is None:
                            temp_pass.append("-")
                        else:
                            temp_pass.append(character)
                    print("".join(temp_pass))
            except ValueError:
                pass
        salt += 1

    password = "".join(found)
    print(f"Password hacked:  {password}")

if __name__ == '__main__':
    part_b()