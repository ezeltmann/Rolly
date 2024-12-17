test_string_1 = "1d6"
test_string_2 = "2d8"
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

set = []
set.append(D6_Test())
set.append(D8_Test())
set.append(D20_Test())
set.append(Mod_Test(4))

for x in set:
    print(x)


