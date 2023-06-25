import discord
import logging
import os

import generator.gen_core
import extras.permastore

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('discord').setLevel(logging.WARN)

store = dict(
    cat1 = [],
    cat2 = [],
    cat3 = []
)

if os.path.exists("store.json"):
    logging.debug("load permastore START")
    store = extras.permastore.load()
    logging.debug("load permastore END")
else:
    logging.warning("permastore loading skipped, no store.json file found")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_message(msg: discord.Message):
    if not msg.author.id == bot.user.id:
        logging.debug("message storage BEGIN")
        split = msg.content.split(' ')

        align0 = int(len(split) * 0)
        align1 = int(len(split) * 0.3334)
        align2 = int(len(split) * 0.6667)
        align3 = int(len(split))
        
        cat1 = split[align0:align1]
        cat2 = split[align1:align2]
        cat3 = split[align2:align3]
        
        logging.debug(f"c1[{len(store['cat1'])}w -> {len(store['cat1']) + len(cat1)}w]")
        logging.debug(f"c2[{len(store['cat2'])}w -> {len(store['cat2']) + len(cat2)}w]")
        logging.debug(f"c3[{len(store['cat3'])}w -> {len(store['cat3']) + len(cat3)}w]")

        store["cat1"] += cat1
        store["cat2"] += cat2
        store["cat3"] += cat3

        logging.debug("disk persist BEGIN")
        extras.permastore.save(store)
        logging.debug("disk persist END")
        logging.debug("message storage END")

@bot.slash_command()
async def generate(ctx: discord.ApplicationContext):
    await ctx.defer()

    logging.debug("START generation")
    try:
        gen = generator.gen_core.try_generate(store)
        if gen == "":
            await ctx.respond("could not generate, try again", ephemeral=True)
            logging.error("empty message")
        else:
            await ctx.respond(gen)
    except Exception as e:
        await ctx.respond(f"failed: {e}")
        logging.error(f"FAILED!! {e}")
    logging.debug("END generation")

with open("token", "r") as file:
    bot.run(file.read())