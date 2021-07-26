import discord
import random
import os
import asyncio
import json
from discord import FFmpegPCMAudio
from discord.utils import get
from discord.ext import commands, tasks
from music_cog import music_cog
from image_cog import image_cog
from itertools import cycle

intents = discord.Intents.all()

client = commands.Bot(command_prefix = ".", intents = intents)
client.add_cog(music_cog(client))
client.add_cog(image_cog(client))
status = cycle(['twitch.tv/panikna','What do you call a cow with no legs? Ground Beef.', 'What do you call a cow in a tornado? A milk shake.', 'What do you call a bear with no teeth? A gummy bear'])


#start
@client.event
async def on_ready():
  change_status.start()
  print("The bot is now ready for use!")
  print("-----------------------------")
@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))
  #moderation
@client.event
async def on_member_join(member):
  role = get(member.guild.roles, name = 'Customer')
  await member.add_roles(role)
  await member.send(f'{member} was given {role}.')

class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
      amount = argument[:-1]
      unit = argument[-1]

      if amount.isdigit() and unit in ['s', 'm','h','d']:
        return(int(amount),unit)
      #musicplayer


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,  guild = ctx.guild)
    if voice.is_playing():
      voice.pause()
    else:
      await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,  guild = ctx.guild)
    if voice.is_paused():
      voice.resume()
    else:
      await ctx.send("The audio is not paused.")
@client.command()
async def leave(ctx):
    if ctx.guild.voice_client.is_connected(): # Checking that they're in a vc
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Sorry, I'm not connected to a voice channel at the moment.")

@client.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect() # This will error if the bot doesn't have sufficient permissions
    else:
        await ctx.send("You're not connected to a channel at the moment.")
@client.command()
async def tempban(ctx, member: discord.Member, duration: DurationConverter):
  multiplier = {'s' : 1, 'm' : 60,'h ': 24, 'd' : 8640}
  amount, unit = duration
  
  await ctx.guild.ban(member)
  await ctx.send(f'{member} has been banned for {amount}{unit}.')
  await asyncio.sleep(amount * multiplier[unit])
  await ctx.guild.unban(member)

@client.command()
async def kick(ctx, member : discord.Member, * , reason = None):
  await member.kick(reason = "Violating the Rules")
  await ctx.send(f'Kicked{member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, * , reason = None):
  await member.ban(reason = "Major Offenses to the Server")
  await ctx.send(f'Banned {member.mention}')
  
@client.command()
async def unban(ctx, * ,member):
  banned_users = await ctx.guild.bans()
  member_name,member_disciminator = member.split('#')

  for ban_entry in banned_users:
      user = ban_entry.user
      
      if(user.name,user.discriminator) == (member_name, member_disciminator):
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned {user.mention}')
        return
@client.command()
@commands.has_permissions(manage_messages= True)
async def clear(ctx, amount = 50):
  await ctx.channel.purge(limit = amount)
  await ctx.send("50 messages removed.")

@client.command()
@commands.has_permissions(manage_messages= True)
async def maxclear(ctx, amount = 100):
  await ctx.channel.purge(limit = amount)
  await ctx.send("100 messages removed.")
  #checksifpersonisrightperson
""""
def is_it_me(ctx):
  return ctx.author.id == 322590872652742657
@client.command()
@commands.check(is_it_me)
async def example(ctx):
  await ctx.send(f'Hi! im {ctx.author}') 
  """
  
  #funcommands
@client.command()
async def ping(ctx):
   await ctx.send(f'Pong! {round(client.latency*1000)}ms')

@client.command(aliases = ['8ball','test'])
async def _8ball(ctx, *, question):
  responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]
  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def hello(ctx):
  await ctx.send("Hello! I am Panik Bot! Pleasure to meet you!")

@client.command()
async def hardware(ctx):
  await ctx.send("Hardware: \n CPU: Intel Core i5-10400F \n GPU: ASUS Dual GeForce RTX 3070 \n MOBO: ASRock B560 Steel Legend \n RAM: Ballistix Sport LT 16GB DDR4")

@client.command()
async def stream(ctx):
  await ctx.send("https://twitch.tv/panikna \n Feel free to drop a follow and a sub! Donations are appreciated! ")
@client.command()
async def about(ctx):
  await ctx.send(" I'm Garret and I love playing games, mostly FPS games like VALORANT. Peak rank is Immortal 1149 and I'm always looking to improve and hit RADIANT. I've been playing games since I was a kid. I love playing FPS games, but am open to anything. Currently looking to stream for fun and get better at VALORANT.")
@client.command()
async def socials(ctx):
  await ctx.send( "https://twitter.com/PANIKval \n https://www.instagram.com/garretduo/ \n https://discord.com/invite/cpXckZ2wTg")

token = ""
with open("token.txt") as file:
  token = file.read()


client.run(token)