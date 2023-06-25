import discord
import random
import logging

logging.basicConfig(level=logging.WARN)

store = dict(
    cat1 = [],
    cat2 = [],
    cat3 = []
)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

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

def try_generate():
    sc1from = int(abs(len(store["cat2"]) + len(store["cat3"])) / len(store["cat1"]))
    sc1to = int(abs(len(store["cat2"]) + len(store["cat3"])) / random.randint(min(2, len(store["cat1"])), len(store["cat1"])))
    sc2from = int(abs(len(store["cat1"]) - len(store["cat3"])) / len(store["cat2"]))
    sc2to = int(abs(len(store["cat1"]) - len(store["cat3"])) / random.randint(min(2, len(store["cat2"])), len(store["cat2"])))
    sc3from = int(abs(len(store["cat1"]) * len(store["cat2"])) / len(store["cat3"]))
    sc3to = int(abs(len(store["cat1"]) * len(store["cat2"])) / random.randint(min(2, len(store["cat3"])), len(store["cat3"])))

    if sc1from > sc1to:
        logging.error("CAT1 RANGE IS INVALID! FROM > TO")
    if sc2from > sc2to:
        logging.error("CAT2 RANGE IS INVALID! FROM > TO")
    if sc3from > sc3to:
        logging.error("CAT3 RANGE IS INVALID! FROM > TO")

    print("-ALIGNMENT-")
    print("C1:", sc1from, "-", sc1to)
    print("C2:", sc2from, "-", sc2to)
    print("C3:", sc3from, "-", sc3to)


    sortedc1 = store["cat1"][
        sc1from:sc1to
    ]

    sortedc2 = store["cat2"][
        sc2from:sc2to
    ]

    sortedc3 = store["cat3"][
        sc3from:sc3to
    ]

    combined = sortedc1 + sortedc2 + sortedc3

    final = str.join(" ", list(dict.fromkeys(combined)))

    return random_transform(final)

@bot.event
async def on_message(msg: discord.Message):
    if not msg.author.id == bot.user.id:
        split = msg.content.split(' ')

        align0 = int(len(split) * 0)
        align1 = int(len(split) * 0.3334)
        align2 = int(len(split) * 0.6667)
        align3 = int(len(split))
        
        cat1 = split[align0:align1]
        cat2 = split[align1:align2]
        cat3 = split[align2:align3]

        store["cat1"] += cat1
        store["cat2"] += cat2
        store["cat3"] += cat3

        print(store)

@bot.slash_command()
async def generate(ctx: discord.ApplicationContext):
    await ctx.defer()

    try:
        gen = try_generate()
        if gen == "":
            await ctx.respond("could not generate, try again", ephemeral=True)
            logging.warn("empty message")
        else:
            await ctx.respond(gen)
    except Exception as e:
        await ctx.respond(f"failed: {e}")

@bot.slash_command()
async def dump(ctx: discord.ApplicationContext):
    await ctx.defer()

    with open("dump.json", "w") as file:
        file.write(str(store))
    
    with open("dump.json", "rb") as file:
        await ctx.respond(file=discord.File(file, "dump.json"))

@bot.slash_command(description="Clears the bot's word memory")
async def lobotomise(ctx: discord.ApplicationContext):
    global store
    await ctx.defer()

    store = dict(
        cat1 = [],
        cat2 = [],
        cat3 = []
    )

    await ctx.respond("ok")

with open("token", "r") as file:
    bot.run(file.read())