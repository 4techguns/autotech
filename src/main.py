import discord
import logging

import generator.gen_core

logging.basicConfig(level=logging.WARN)

store = dict(
    cat1 = [],
    cat2 = [],
    cat3 = []
)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

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
        gen = generator.gen_core.try_generate(store)
        if gen == "":
            await ctx.respond("could not generate, try again", ephemeral=True)
            logging.warning("empty message")
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