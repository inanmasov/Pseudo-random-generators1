import random
import json
import time

class DynamicShiftRegisterGenerator:
    def __init__(self, a, b, x0):
        binary_string = bin(a)[2:]
        binary_string = binary_string.zfill(64)
        self.a = [int(bit) for bit in binary_string]

        binary_string = bin(b)[2:]
        binary_string = binary_string.zfill(64)
        self.b = [int(bit) for bit in binary_string]

        self.x0 = x0

    def generate(self, n):
        x = self.x0
        sequence = [x]
        for _ in range(n - 1):
            fa0 = 0
            fa1 = 0
            for i in range(len(self.a) - 1, -1, -1):
                if i % 2 == 0:
                    fa0 += (self.a[i]*pow(x, i))
                else:
                    fa1 += (self.a[i]*pow(x, i))
            fa0 = fa0 % 2**len(self.a) - 1
            fa1 = fa1 % 2 ** len(self.a) - 1

            fb0 = 0
            fb1 = 0
            for i in range(len(self.b) - 1, -1, -1):
                if i % 2 == 0:
                    fb0 += (self.b[i]*pow(x, i))
                else:
                    fb1 += (self.b[i]*pow(x, i))
            fb0 = fb0 % 2 ** len(self.b) - 1
            fb1 = fb1 % 2 ** len(self.b) - 1

            x = (fa1*fb1 - fa0*fb0) % 2**len(self.a) - 1
            self.shift_registers()
            sequence.append(x)
    
        return sequence

    def shift_registers(self):
        new_value1 = 0
        new_value2 = 0

        for i in range(len(self.a) - 1, 0, -1):
            new_value1 += self.a[i]
            self.a[i] = self.a[i - 1]

        for i in range(len(self.b) - 1, 0, -1):
            new_value2 += self.b[i]
            self.b[i] = self.b[i - 1]

        self.a[0] = (self.a[0] + new_value1) % 2
        self.b[0] = (self.b[0] + new_value2) % 2


def CongruentGeneratorK2():
    mode = int(input("Выберите режим работы:\n1 - Случайный выбор параметров\n2 - Пользовательский ввод параметров\n3 - Чтение из конфигурационного файла\n"))
    x0, a, b, length = 0, 0, 0, 0
    if mode == 1:
        x0 = random.randint(2**63, 2 ** 64 - 1)
        a = random.randint(2**63, 2 ** 64 - 1)
        b = random.randint(2**63, 2 ** 64 - 1)
        print("Сгенерированные параметры:")
        print("x0:", x0)
        print("a:", a)
        print("b:", b)
        length = int(input("Введите длину выходной последовательности: "))
    elif mode == 2:
        x0 = int(input("Введите начальное значение (x0): "))
        a = int(input("Введите значение 1 вектора (a): "))
        b = int(input("Введите значение 2 вектора (b): "))
        length = int(input("Введите длину выходной последовательности: "))
    elif mode == 3:
        with open("config1.txt", 'r') as file:
            config = json.load(file)
        x0 = config['x0']
        a = config['a']
        b = config['b']
        length = config['l']
    else:
        return

    generator = DynamicShiftRegisterGenerator(a, b, x0)
    start_time = time.time()
    random_sequence = generator.generate(length)
    print(time.time() - start_time)

    with open("random_sequence1.txt", "w") as file:
        file.write(str(random_sequence))

    out_sec_bin = ''
    for i in random_sequence:
        out_sec_bin += bin(i)[2:]

    with open("out_seq_bin1.txt", "w") as file:
        file.write(out_sec_bin)

class LinearCongruentialGenerator:
    def __init__(self, x0, a, c, N):
        self.x0 = x0
        self.a = a
        self.c = c
        self.N = N

    def generate(self, n):
        x = self.x0
        result = [x]
        for _ in range(n - 1):
            x = (self.a * x + self.c) % self.N
            result.append(x)
        return result

def generate_random_parameters():
    x0 = random.randint(2**63, 2**64 - 1)
    a = random.randint(2**63, 2**64 - 1)
    c = random.randint(2**63, 2**64 - 1)
    m = random.choice([2**63 - 1, 2**64 - 1]) 
    return x0, a, c, m

def MixedCongruentGenerator():
    mode = int(input("Выберите режим работы:\n1 - Случайный выбор параметров\n2 - Пользовательский ввод параметров\n3 - Чтение из конфигурационного файла\n"))
    x0, a, c, N, length = 0, 0, 0, 0, 0
    if mode == 1:
        x0, a, c, N = generate_random_parameters()
        print("Сгенерированные параметры:")
        print("x0:", x0)
        print("a:", a)
        print("c:", c)
        print("N:", N)
        length = int(input("Введите длину выходной последовательности: "))
    elif mode == 2:
        x0 = int(input("Введите начальное значение (x0): "))
        a = int(input("Введите множитель (a): "))
        c = int(input("Введите приращение (c): "))
        N = int(input("Введите модуль (N): "))
        length = int(input("Введите длину выходной последовательности: "))
    elif mode == 3:
        with open("config.txt", 'r') as file:
            config = json.load(file)
        x0 = config['x0']
        a = config['a']
        c = config['c']
        N = config['N']
        length = config['l']
    else:
        return

    generator = LinearCongruentialGenerator(x0, a, c, N)
    start_time = time.time()
    random_sequence = generator.generate(length)
    print(time.time() - start_time)

    with open("random_sequence.txt", "w") as file:
        file.write(str(random_sequence))

    out_sec_bin = ''
    for i in random_sequence:
        out_sec_bin += bin(i)[2:]

    with open("out_seq_bin.txt", "w") as file:
        file.write(out_sec_bin)

def main():
    typeGenerator = int(input("Введите номер генератора (1, 2): "))
    if typeGenerator == 1:
        MixedCongruentGenerator()
    if typeGenerator == 2:
        CongruentGeneratorK2()

def test_time():
    all_time1 = 0
    all_time2 = 0
    count_test = 100
    length= 10000
    for _ in range(count_test):
        x0, a, c, N = generate_random_parameters()
        generator = LinearCongruentialGenerator(x0, a, c, N)
        start_time = time.time()
        random_sequence = generator.generate(length)
        end_time = time.time() - start_time
        all_time1 += end_time

        x0 = random.randint(2**63, 2 ** 64 - 1)
        a = random.randint(2**63, 2 ** 64 - 1)
        b = random.randint(2**63, 2 ** 64 - 1)
        generator = DynamicShiftRegisterGenerator(a, b, x0)
        start_time = time.time()
        random_sequence = generator.generate(length)
        end_time = time.time() - start_time
        all_time2 += end_time

    print("1 generator: ", all_time1 / count_test)
    print("2 generator: ", all_time2 / count_test)

if __name__ == "__main__":
    #test_time()
    main()