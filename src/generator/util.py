import random

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

def random_transform(inp: str):
    r = random.randint(0, 4)
    rc = random.randint(0, 3)

    if inp == "":
        return ""
   
    input = inp

    if rc == 1:
        input = input.lower().capitalize()
    elif rc == 2:
        input = input.lower()
    elif rc == 3:
        input = input.upper()

    if r == 0: # default
        return input
    elif r == 1: # period at end
        return input + "."
    elif r == 2: # exclamation at end
        return input + "!"
    elif r == 3: # questionmark at end
        return input + "?"
    elif r == 4: # ellipsis
        return input + "..."