import discord
import logging
import os

import generator.gen_core
import extras.permastore

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('discord').setLevel(logging.WARN)

gstore = dict()

if os.path.exists("store.json"):
    logging.debug("load permastore START")
    gstore = extras.permastore.load()
    logging.debug("load permastore END")
else:
    logging.warning("permastore loading skipped, no store.json file found")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_message(msg: discord.Message):
    if not msg.author.id == bot.user.id:
        if not msg.guild.id in gstore:
            logging.warning(f"no store for guild {msg.guild.id}; creating")
            gstore[msg.guild.id] = dict(
                cat1 = [],
                cat2 = [],
                cat3 = []
            )

        if f"<@{bot.user.id}>" in msg.content:

            logging.debug("ping generation trigger")
            logging.debug("START generation")

            msg.channel.trigger_typing()

            try:
                gen = generator.gen_core.try_generate(gstore[msg.guild.id])
                if gen == "":
                    logging.error("empty message")
                else:
                    await msg.reply(gen)
            except Exception as e:
                logging.error(f"FAILED!! {e}")
            logging.debug("END generation")


        logging.debug("message storage BEGIN")
        split = msg.content.split(' ')

        align0 = int(len(split) * 0)
        align1 = int(len(split) * 0.3334)
        align2 = int(len(split) * 0.6667)
        align3 = int(len(split))
        
        cat1 = split[align0:align1]
        cat2 = split[align1:align2]
        cat3 = split[align2:align3]
        
        logging.debug(f"c1[{len(gstore[msg.guild.id]['cat1'])}w -> {len(gstore[msg.guild.id]['cat1']) + len(cat1)}w]")
        logging.debug(f"c2[{len(gstore[msg.guild.id]['cat2'])}w -> {len(gstore[msg.guild.id]['cat2']) + len(cat2)}w]")
        logging.debug(f"c3[{len(gstore[msg.guild.id]['cat3'])}w -> {len(gstore[msg.guild.id]['cat3']) + len(cat3)}w]")

        gstore[msg.guild.id]["cat1"] += cat1
        gstore[msg.guild.id]["cat2"] += cat2
        gstore[msg.guild.id]["cat3"] += cat3

        logging.debug("disk persist BEGIN")
        extras.permastore.save(gstore)
        logging.debug("disk persist END")
        logging.debug("message storage END")

@bot.slash_command()
async def generate(ctx: discord.ApplicationContext):
    await ctx.defer()

    logging.debug("START generation")
    try:
        gen = generator.gen_core.try_generate(gstore[ctx.guild.id])
        if gen == "":
            await ctx.respond("could not generate, try again", ephemeral=True)
            logging.error("empty message")
        else:
            await ctx.respond(gen)
    except Exception as e:
        await ctx.respond(f"failed: {e}")
        logging.error(f"FAILED!! {e}")
    logging.debug("END generation")

@bot.slash_command()
async def generate_debug(ctx: discord.ApplicationContext):
    await ctx.defer()

    logging.debug("START generation")
    try:
        gen = generator.gen_core.try_generate_dbg(gstore[ctx.guild.id])
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