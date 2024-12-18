import re

test_string_1_0 = "1d6"
test_string_1_1 = "1d8"
test_string_1_2 = "1d20"
test_string_2_0 = "2d6"
test_string_2_1 = "2d8"
test_string_2_2 = "2d20"
test_string_3 = "1d20 + 5"
test_string_4 = "1d20 - 5"
test_string_5 = "1d6 + 1d20"

class Die_Test():
    def __init__(self):
        pass

class D6_Test(Die_Test):
    def __init__(self):
        self.type = "d6"

    def __str__(self):
        return self.type

class D8_Test(Die_Test):
    def __init__(self):
        self.type = "d8"

    def __str__(self):
        return self.type

class D20_Test(Die_Test):
    def __init__(self):
        self.type = "d20"

    def __str__(self):
        return self.type

class Mod_Test(Die_Test):
    def __init__(self, value):
        self.type = "Mod"
        self.value = value

    def __str__(self):
        return self.type + ' Value: ' + str(self.value)

def use_regex(input_text):
    pattern = re.compile(r"[0-9]+d[0-9]+", re.IGNORECASE)
    return pattern.match(input_text).string

def get_dice_list(input_string):
    roll = use_regex(input_string)
    (count, d_type) = roll.lower().split('d')
    dice_list = []
    for d in range(0,int(count)):
        if d_type == '6':
            dice_list.append(D6_Test())
        elif d_type == '8':
            dice_list.append(D8_Test())
        elif d_type == '20':
            dice_list.append(D20_Test())
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
#die_tester(test_string_3)
#die_tester(test_string_4)
#die_tester(test_string_5)