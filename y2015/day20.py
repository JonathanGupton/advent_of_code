    from sympy import divisors

    puzzle_input = 36000000


    def part_a() -> int:
        global puzzle_input
        h = 1
        while True:
            output = sum([i * 10 for i in divisors(h, generator=True)])
            if output > puzzle_input: return h
            h += 1


    def part_b(part_a_result: int):
        global puzzle_input
        n = part_a_result
        max_houses = 50
        while True:
            presents = 0
            d = divisors(n)
            for i in d[::-1]:
                if i * max_houses > n:
                    presents += i * 11
                else:
                    break
            if presents > puzzle_input:
                return n
            else:
                n += 1


    if __name__ == '__main__':
        part_a_result = part_a()
        print(part_a_result)
        print(part_b(part_a_result))
