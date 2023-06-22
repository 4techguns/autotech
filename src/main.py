import discord
import random
import logging

logging.basicConfig(level=logging.DEBUG)

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

    input = inp

    if rc == 1:
        input = input.capitalize()
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
    sortedc1 = store["cat1"][
        int(abs(len(store["cat2"]) + len(store["cat3"])) / len(store["cat1"]))
        :
        int(abs(len(store["cat2"]) + len(store["cat3"])) / random.randint(min(2, len(store["cat1"])), len(store["cat1"])))
    ]

    sortedc2 = store["cat2"][
        int(abs(len(store["cat1"]) - len(store["cat3"])) / len(store["cat2"]))
        :
        int(abs(len(store["cat1"]) - len(store["cat3"])) / random.randint(min(2, len(store["cat2"])), len(store["cat2"])))
    ]

    sortedc3 = store["cat3"][
        int(abs(len(store["cat1"]) * len(store["cat2"])) / len(store["cat3"]))
        :
        int(abs(len(store["cat1"]) * len(store["cat2"])) / random.randint(min(2, len(store["cat3"])), len(store["cat3"])))
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