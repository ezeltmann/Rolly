def foo(**kwargs):
    foo2(**kwargs)
    for entry in kwargs.items():
        print("Key: {}, value: {}".format(entry[0], entry[1]))

def foo2(**kwargs):
    for entry in kwargs.items():
        if entry[0] == 'd':
            for entry2 in entry[1].items():
                print("Kwarg2 = Key: {}, value: {}".format(entry2[0], entry2[1]))

# call using normal keys:
foo(a=1, b=2, c=3)
# call using an unpacked dictionary:
foo(**{"a": 1, "b":2, "c":3, "d":{"e":5,"f":6}})

# call using a dictionary fails because the function will think you are
# giving it a positional argument
#foo({"a": 1, "b": 2, "c": 3})
# this yields the same error as any other positional argument
#foo(3)
#foo("string")