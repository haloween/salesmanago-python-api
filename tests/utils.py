import random
import string


def gen_string(length, characters=None):
    if not characters:
        characters = string.ascii_letters+string.digits
    
    fn=''
    for i in range(length):
        fn+=random.choice(characters)

    return fn

def gen_list_of_strings(length):
    return [gen_string(random.randint(4,12)) for i in range(length)]

def gen_dict(length):
    return {gen_string(random.randint(4,12)):gen_string(random.randint(4,12)) for i in range(length)}

def gen_true_false():
    randval = random.randint(1,100)
    return True if randval > 50 else False