import discord
from discord.ext import commands
import asyncio
import re
import uuid

bot = commands.Bot(command_prefix = "!")
print("Set prefix.")

@bot.event
async def on_ready():
    print("Logged in as:")
    print(bot.user.name)
    print("ID:")
    print(bot.user.id)
    emb = discord.Embed(description = "I am now online, protecting (JB) jetBlue Airways ®!", colour = 0x00FF00)
    await bot.send_message(bot.get_channel("282946350742634496"), embed = emb)
    emb = discord.Embed(description = "Logs successfully synchronized!", colour = 0x00FF00)
    await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)
    print("Ready to use!")

admins = ["britishlieutenant#0009", "AvionBlue#0945", "FlyGuyKrystian11235#2961", "what is goin on folks Aa#6858", "Jeren3333#0296", "JoshAviation#4754", "Uni#0870"]
commands = ["!ping", "!prefix", "!purge", "!kick", "!ban", "!mute", "!unmute", "!announce", "!update", "!report", "!cmds"]

@bot.command()
async def prefix():
    emb = discord.Embed(description = "Prefix: !", colour = 0x000080)
    await bot.say(embed = emb)

@bot.command(pass_context = True)
async def purge(ctx, amount: int = None):
    if str(ctx.message.author) in admins:
        if amount == None:
            await bot.say("You must specify an amount of messages to purge.")
        else:
            await bot.purge_from(ctx.message.channel, limit = amount)
            message = await bot.say("Purged {} messages.".format(amount))
            await asyncio.sleep(3)
            await bot.delete_message(message)
            emb = discord.Embed(description = "Purged {} messages.".format(amount), colour = 0x000080)
            emb.set_author(name = str(ctx.message.author))
            await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member = None):
    if str(ctx.message.author) in admins:
        if member == None:
            await bot.say("You must specify a user to kick.")
        else:
            await bot.kick(member)
            emb = discord.Embed(description = "Kicked {}.".format(str(member)), colour = 0x000080)
            emb.set_author(name = str(ctx.message.author))
            await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def ban(ctx, member: discord.Member = None):
    if str(ctx.message.author) in admins:
        if member == None:
            await bot.say("You must specify a user to ban.")
        else:
            await bot.ban(member)
            emb = discord.Embed(description = "Banned {}.".format(str(member)), colour = 0x000080)
            emb.set_author(name = str(ctx.message.author))
            await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def mute(ctx, member: discord.Member = None):
    if str(ctx.message.author) in admins:
        if member == None:
            await bot.say("You must specify a user to mute.")
        else:
            await bot.add_roles(member, discord.utils.get(ctx.message.server.roles, name = "Muted"))
            emb = discord.Embed(description = "Muted {}.".format(str(member)), colour = 0x000080)
            emb.set_author(name = str(ctx.message.author))
            await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def unmute(ctx, member: discord.Member = None):
    if str(ctx.message.author) in admins:
        if member == None:
            await bot.say("You must specify a user to unmute.")
        else:
            await bot.remove_roles(member, discord.utils.get(member.roles, name = "Muted"))
            emb = discord.Embed(description = "Unmuted {}.".format(str(member)), colour = 0x000080)
            emb.set_author(name = str(ctx.message.author))
            await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def announce(ctx):
    if str(ctx.message.author) in admins:
        msg = ctx.message.content[9:]
        emb = discord.Embed(description = msg, color = 0x000080)
        emb.set_author(name = "ANNOUNCEMENT:")
        await bot.send_message(bot.get_channel("282974478689107969"), "@everyone")
        await bot.send_message(bot.get_channel("282974478689107969"), embed = emb)
        emb = discord.Embed(description = "Announce message sent.", colour = 0x000080)
        emb.set_author(name = str(ctx.message.author))
        await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def update(ctx):
    if str(ctx.message.author) in admins:
        msg = ctx.message.content[8:]
        emb = discord.Embed(description = msg, color = 0x000080)
        emb.set_author(name = "UPDATE:")
        await bot.send_message(bot.get_channel("282974478689107969"), "@everyone")
        await bot.send_message(bot.get_channel("282974478689107969"), embed = emb)
        emb = discord.Embed(description = "Update message sent.", colour = 0x000080)
        emb.set_author(name = str(ctx.message.author))
        await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.command(pass_context = True)
async def report(ctx):
    await bot.say("Hello. Who would you like to report?")
    suspect = await bot.wait_for_message(author = ctx.message.author, timeout = 10)
    await bot.say("Why would you like to report them?")
    reason = await bot.wait_for_message(author = ctx.message.author, timeout = 10)
    await bot.say("Thank you. Your report will be reviewed shortly.")
    await bot.send_message(bot.get_channel("383666253497106435"), "**SUSPECT**: {}".format(suspect.content))
    await bot.send_message(bot.get_channel("383666253497106435"), "**REASON**: {}".format(reason.content))

async def watch_profanity(message):
    compressed = message.content.replace(' ','').replace('-','').replace('_','').replace('^','').replace('\'','').replace('\"','').replace('=','').replace('*','')
    uid = uuid.uuid4()
    with open('profanity.exp.txt','r') as f:
        for reg in f:
            reg = reg.strip()
            exp = re.search(reg,compressed)
            if exp: ## perform a regex search for illicit terms
                print('{} term detected at {} (UUID {})'.format(exp.group(),message.author.name,uid))
                await bot.delete_message(message)
                return

@bot.command(pass_context = True)
async def cmds(ctx):
    if str(ctx.message.author) in admins:
        emb = discord.Embed(description = "kick\nban\nmute\nunmute\npurge\nannounce\nupdate", colour = 0x000080)
        emb.set_author(name = "Commands")
        await bot.say(embed = emb)
    else:
        await bot.say("You cannot use this command because you're not a moderator! :rolling_eyes:")

@bot.event
async def on_message(message):
    if str(message.author) == "Blue Bot#9897":
        return
    else:
        if message.content == "C:" or message.content == ":C" or message.content == "D:" or message.content == ":D" or message.content == ":O" or message.content == "O:" or message.content == ":P" or message.content == "XD" or message.content == ":)" or message.content == ":(":
            return
        elif message.content.isupper() == True:
            await bot.delete_message(message)
        elif "https://" in message.content:
            await bot.delete_message(message)
        elif message.content == "<@381385380974297091>":
            emb = discord.Embed(description = "Status: ONLINE", colour = 0x00FF00)
            await bot.send_message(message.channel, embed = emb)
        elif message.content.startswith("!"):
            wordList = message.content.split(" ")
            firstWord = wordList[0]
            print(firstWord)
            if message.content == "!help":
                return
            if not firstWord in commands:
                emb = discord.Embed(description = "It appears that this command does not exist!", colour = 0xFF0000)
                emb.set_author(name = "Error!")
                await bot.send_message(message.channel, embed = emb)
    await watch_profanity(message)
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if str(message.author) == "Blue Bot#9897":
        return
    else:
        emb = discord.Embed(description = "Message deleted:\n{}".format(message.content), colour = 0x000080)
        emb.set_author(name = str(message.author))
        await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.event
async def on_member_join(member):
    emb = discord.Embed(description = "Welcome <@{}>! Remember to read the rules, and have a great time here at jetBlue!".format(str(member.id)), colour = 0x000080)
    emb.set_author(name = str(member))
    await bot.send_message(bot.get_channel("282946350742634496"), embed = emb)
    emb = discord.Embed(description = "{} joined.".format(str(member)), colour = 0x000080)
    emb.set_author(name = str(member))
    await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

@bot.event
async def on_member_remove(member):
    emb = discord.Embed(description = "<@{}> left! What a shame!".format(str(member.id)), colour = 0x000080)
    emb.set_author(name = str(member))
    await bot.send_message(bot.get_channel("282946350742634496"), embed = emb)
    emb = discord.Embed(description = "{} left.".format(str(member)), colour = 0x000080)
    emb.set_author(name = str(member))
    await bot.send_message(bot.get_channel("383760579166208000"), embed = emb)

bot.run("MzgxMzg1MzgwOTc0Mjk3MDkx.DPMVfw.z2k8ifshQtwLiPOsv1jFcuQwC9c")
