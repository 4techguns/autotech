import random

punc = ["", ".", "!", "?", "...", "?!"]

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

def random_transform(inp: str):
    rc = random.randint(0, 3)

    if len(inp) == 0: return ""
   
    input = inp

    if rc == 1:
        input = input.lower().capitalize()
    elif rc == 2:
        input = input.lower()
    elif rc == 3:
        input = input.upper()

    return input + random.choice(punc)