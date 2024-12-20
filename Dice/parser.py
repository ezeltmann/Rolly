import re
import D6
import D8
import D20
import Modifier








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
                    dice_list.append(D6())
                elif d_type == '8':
                    dice_list.append(D8())
                elif d_type == '20':
                    dice_list.append(D20())
        else:
            value = int(item)
            if (negative):
                value = value*-1
            result = Modifier()
            result.value = value
            dice_list.append(result)

    return dice_list