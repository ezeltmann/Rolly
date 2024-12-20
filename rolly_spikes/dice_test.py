import re

test_string_1_0 = "1d6"
test_string_1_1 = "1d8"
test_string_1_2 = "1d20"
test_string_2_0 = "2d6"
test_string_2_1 = "2d8"
test_string_2_2 = "2d20"
test_string_3_0 = "1d20 + 5"
test_string_3_1 = "1d20+5"
test_string_3_2 = "1d20 +5"
test_string_3_3 = "1d20+ 5"
test_string_4_0 = "1d20 - 5"
test_string_4_1 = "1d20-5"
test_string_4_2 = "1d20- 5"
test_string_4_3 = "1d20 -5"
test_string_5_0 = "1d6 + 1d20"
test_string_5_1 = "1d6 - 1d20"
test_string_5_2 = "1d6 + 1d20 - 5"

class Die_Test():
    def __init__(self, neg):
        self.neg = neg
        pass

class D6_Test(Die_Test):
    def __init__(self, neg):
        super().__init__(neg)
        self.type = "d6"

    def __str__(self):
        return self.type + ' Negative: ' + str(self.neg)

class D8_Test(Die_Test):
    def __init__(self, neg):
        super().__init__(neg)
        self.type = "d8"

    def __str__(self):
        return self.type + ' Negative: ' + str(self.neg)

class D20_Test(Die_Test):
    def __init__(self, neg):
        super().__init__(neg)
        self.type = "d20"

    def __str__(self):
        return self.type + ' Negative: ' + str(self.neg)

class Mod_Test(Die_Test):
    def __init__(self, value):
        self.type = "Mod"
        self.value = value

    def __str__(self):
        return self.type + ' Value: ' + str(self.value)

def use_regex(input_text):
    pattern = re.compile(r"[0-9]+d[0-9]+", re.IGNORECASE)
    return pattern.match(input_text)

def find(s, ch1, ch2):
    return [i for i, ltr in enumerate(s) if (ltr == ch1) or (ltr == ch2)]

def split_multiple(input_string):
    indicies = find(input_string, "+", "-")
    results = []
    start = 0

    if (indicies is not None):
        for index in indicies:
            results.append(input_string[start:index])
            start = index

    results.append(input_string[start:])
    return results

def get_dice_list(input_string):
    input_string = input_string.replace(" ","")
    items = split_multiple(input_string)
    dice_list = []

    for item in items:
        negative = item.startswith("-")
        item = item.replace("+","")
        item = item.replace("-","")
        roll = use_regex(item)
        if (roll is not None):
            (count, d_type) = roll.string.lower().split('d')
            for d in range(0,int(count)):
                if d_type == '6':
                    dice_list.append(D6_Test(negative))
                elif d_type == '8':
                    dice_list.append(D8_Test(negative))
                elif d_type == '20':
                    dice_list.append(D20_Test(negative))
        else:
            value = int(item)
            if (negative):
                value = value*-1
            dice_list.append(Mod_Test(value))

    return dice_list

def print_dice_list(dice_list):
    for x in dice_list:
        print(x)


def die_tester(input_string):
    dice_list = []
    dice_list = get_dice_list(input_string)
    print("We should get something like: " + input_string)
    print_dice_list(dice_list)

die_tester(test_string_1_0)
die_tester(test_string_1_1)
die_tester(test_string_1_2)
die_tester(test_string_2_0)
die_tester(test_string_2_1)
die_tester(test_string_2_2)
die_tester(test_string_3_0)
die_tester(test_string_3_1)
die_tester(test_string_3_2)
die_tester(test_string_3_3)
die_tester(test_string_4_0)
die_tester(test_string_4_1)
die_tester(test_string_4_2)
die_tester(test_string_4_3)
die_tester(test_string_5_0)
die_tester(test_string_5_1)
die_tester(test_string_5_2)