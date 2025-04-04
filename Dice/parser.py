import re
from Dice.D2 import D2
from Dice.D3 import D3
from Dice.D4 import D4
from Dice.D6 import D6
from Dice.D8 import D8
from Dice.D10 import D10
from Dice.D12 import D12
from Dice.D20 import D20
from Dice.D100 import D100
from Dice.Modifier import Modifier



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

def get_dice_list(input_string, base):
    input_string = input_string.replace(" ","")
    items = split_multiple(input_string)
    dice_list = []

    for item in items:
        negative = item.startswith("-")
        item = item.replace("+","")
        item = item.replace("-","")
        if (item.startswith('d') or item.startswith('D')):
            item = "1"+item
        roll = use_regex(item)
        if (roll is not None):
            (count, d_type) = roll.string.lower().split('d')
            if int(count) > 100:
                count = '100'
            for d in range(0,int(count)):
                die = None
                if d_type == '2':
                    die = D2("models/dice/d2.gltf")
                elif d_type == '3':
                    die = D3("models/dice/d3.gltf")
                elif d_type == '4':
                    die = D4("models/dice/d4.gltf")
                elif d_type == '6':
                    die = D6("models/dice/d6_num.gltf")
                elif d_type == '8':
                    die = D8("models/dice/d8.gltf")
                elif d_type == '10':
                    die = D10("models/dice/d10.gltf")
                elif d_type == '12':
                    die = D12("models/dice/d12.gltf")
                elif d_type == '20':
                    die = D20("models/dice/d20.gltf")
                elif d_type == '100':
                    die = D100("models/dice/d100.gltf")
                die.die_setup(base.render, base.loader)
                dice_list.append(die)

        else:
            if not (item == ""):
                value = int(item)
                if (negative):
                    value = value*-1
                result = Modifier()
                result.value = value
                result.die_setup(base.render, base.loader)
                dice_list.append(result)

    return dice_list