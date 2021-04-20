import discord, io, asyncio, aiohttp
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from random import randint
import random
import asyncio
import aiohttp
from discord import Guild, Member, Embed
from discord.utils import get
import akinator as ak
# Do not remove credits or you will be sued by me bitches :-)
token = 'token here'
Bot_name = 'Bobert'

client = commands.Bot(command_prefix="f!")
client.remove_command('help')

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("f!invite | f!help"))

@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandNotFound):
    await ctx.send('**This Command Does not exist dum dum.**')

room = {}
my_id = 825972660554170368 # YOUR BOT ID IN HERE
map_game = Image.open("./image/map.png").convert("RGBA")
size = map_game.size
coordinate = {
  0 : (64, 1300),
  1 : (208, 1120),
  2 : (278, 1045),
  3 : (190, 915),
  4 : (316, 913),
  5 : (348, 811),
  6 : (377, 707),
  7 : (412, 595),
  8 : (343, 522),
  9 : (426, 436),
  10 : (367, 343),
  11 : (217, 336),
  12 : (243, 210),
  13 : (434, 129),
  14 : (473, 263),
  15 : (539, 353),
  16 : (634, 449),
  17 : (752, 370),
  18 : (827, 288),
  19 : (870, 203),
  20 : (1009, 210),
  21 : (1222, 136),
  22 : (1031, 354),
  23 : (918, 389),
  24 : (820, 472),
  25 : (896, 595),
  26 : (1073, 591),
  27 : (1182, 714),
  28 : (1138, 875),
  29 : (1141, 978),
  30 : (1197, 1050),
  31 : (1035, 1077),
  32 : (969, 963),
  33 : (920, 869),
  34 : (808, 926),
  35 : (774, 786),
  36 : (750, 666),
  37 : (605, 670),
  38 : (554, 786),
  39 : (536, 926),
  40 : (428, 1007)}
words = [
  "Fell into a hole somewhere",
  "Banana slips",
  "Thrown by the wind",
  "His tongue was bitten",
  "His feet don't want to follow his wishes"]
no_reakt = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(5)]

def resize(scale, image):
  scaled_size = tuple([x * scale for x in image.size])
  image2 = image.resize(scaled_size)
  return image2

async def zooms(file, no=0):
  img = Image.open(file).convert("RGBA")
  w, h = img.size
  img2 = resize(2, img)

  files = io.BytesIO()

  if no == 1:
    img3 = img2.crop((0, 0, w, h))
    img3.save(files, format="PNG")
  elif no == 2:
    img3 = img2.crop((w, 0, img2.width, h))
    img3.save(files, format="PNG")
  elif no == 3:
    img3 = img2.crop((0, h, w, img2.height))
    img3.save(files, format="PNG")
  elif no == 4:
    img3 = img2.crop((w, h, img2.width, img2.height))
    img3.save(files, format="PNG")
  files.seek(0)
  return files

async def reakt(chat):
  await chat.add_reaction("🎲")  # Dice
  await chat.add_reaction("❌")  # exit
  for i in no_reakt:
    await chat.add_reaction(i)

async def skill_2(self, game):
  channel = client.get_channel(game.get_room_id())
  chat = await channel.send(f"> `Mention/tag someone`")
  players = game.list_player()

  def chek(message):
    if message.author.id == self.player_id:
      return True

  while True:
    try:
      message = await client.wait_for("message", timeout=60, check=chek)
    except asyncio.TimeoutError:
      await chat.delete()
      break
    else:
      mentioned = message.mentions
      if mentioned:
        for pl in players:
          if pl.player_id != self.player_id:
            if pl.player_id == mentioned[0].id:
              pl.position -= 5
              if pl.position < 0:
                pl.position = 0
              await chat.edit(content=f"> `{pl.player_name} {words[randint(0,4)]}`\n> `so that makes him walk 5 Step Backward`")
              await asyncio.sleep(3)
              await chat.delete()
              break

class GameSnL():
  def __init__(self, channel_id):
    self.room_id = channel_id
    self.start = False
    self.player = []
    self.__turns = 0

  def get_room_id(self):
    return self.room_id

  def game_state(self):
    return self.start

  def join(self, player_obj):
    self.player.append(player_obj)

  def list_player(self):
    return self.player

  def dice(self, player):
    roll = randint(1,6)
    return roll

  def get_turns(self):
    return self.__turns

  def update_turns(self):
    self.__turns += 1
    if self.__turns > len(self.player)-1:
      self.__turns = 0
    return self.__turns

  def skill_1(self):
    self.__turns -= 1
    if self.__turns < 0:
      self.__turns = len(self.player)-1

  def game_start(self):
    self.start = True

  def game_stop(self):
    self.start = False

class Player():
  def __init__(self, user, room):
    self.player_name = user.display_name
    self.avatar = user.avatar_url
    self.player_id = user.id
    self.room_id = room
    self.position = 0
    self.skill = 0
    self.skill_done = 0
    self.nameSkill = {
      1: "***`Time Travel Skill 🕙 - Back to The Past`***",
      2: "***`Punishment Skill 👊 - 5 Step Backward to Someone`***"}

  def update_position(self, pos):
    self.position += pos

  def gacha_skill(self):
    chance = randint(0, 100)

    if self.skill_done == 1:
      chance += 50
    elif self.skill_done == 2:
      chance += 80
    elif self.skill_done > 2:
      chance = 0
      self.skill_done = 0

    if chance <= 100 and chance > 29:
      self.skill = randint(0,2)
      self.skill_done += 1
      return
    self.skill = 0

  async def skill_activate(self, game):
    if self.skill == 1:
      game.skill_1()
    elif self.skill == 2:
      await skill_2(self, game)
    x = f"> `Skill `{self.nameSkill[self.skill]}` has been used`"
    return x

async def get_image(player):
  async with aiohttp.ClientSession() as session:
    async with session.get(str(player.avatar)) as r:
      file = io.BytesIO(await r.read())
      img = Image.open(file).convert("RGBA")
      img.thumbnail((32, 32))
    return img

async def Screen(game, player_now=None):
  mapnya = Image.new("RGBA", size)
  mapnya.paste(map_game)
  player = game.list_player()
  addCor = 16

  for pl in player:
    avatar = await get_image(pl)
    x, y = coordinate[pl.position]
    position = (x,y)
    if player_now:
      if player_now.player_id != pl.player_id:
        if player_now.position == pl.position:
          position = (x + addCor, y)
          addCor += 16
    mapnya.paste(avatar, position, avatar)

  file = io.BytesIO()
  mapnya.save(file, format="PNG")
  file.seek(0)
  return file

async def render_map(channel, screenss, game):
  players = game.list_player()
  embed = discord.Embed(
    title=f"**Room {channel.name}**",
    color=discord.Colour(0x3498db),
    description="🐍 `Map` 🎲")
  embed.set_image(url="attachment://map.png")
  for pl in players:
    embed.add_field(name=f"**{pl.player_name}**", value=f"⏩ = ***`{pl.position}`***" + "-"*5)
  embed.add_field(name=f"**===============**", value=f"***`Turn`*** = ***`{players[game.get_turns()].player_name}`***", inline=False)
  chat = await channel.send(file=discord.File(screenss, "map.png") , embed=embed)
  return chat

async def skill_want_to_activate(player_now, info, game, channal):
  if player_now.skill != 0:
    await info.edit(content=f"> `{player_now.player_name} Got` {player_now.nameSkill[player_now.skill]}\n> `Want to use` ?")
    await info.add_reaction("🇾") # YES
    await info.add_reaction("🇳") # NO

    def chek(reaction, user):
      if user.id == player_now.player_id and reaction.message.id == info.id:
        return True
    while True:
      try:
        reaction, user = await client.wait_for("reaction_add", timeout=60, check=chek)
      except asyncio.TimeoutError:
        await info.clear_reactions()
        break
      else:
        await info.clear_reactions()
        if str(reaction.emoji) == "🇾":  # Yes
          xxx = await player_now.skill_activate(game)
          info3 = await channal.send(xxx)
          await asyncio.sleep(2)
          await info3.delete()
          break
        elif str(reaction.emoji) == "🇳":  # NO
          break

async def win_won(game, player, channel):
  champions = {}

  for pl in game.list_player():
    if pl.player_id != player.player_id:
      champions[pl.player_name] = pl.position

  sorting = reversed(sorted(champions.keys()))
  number = 2

  embed = discord.Embed(
    title=f" 👑 **The Winner is** {player.player_name} ",
    color=discord.Colour(0x3498db),
    description="🐍 **Congratulations for winning the game** 🥳")
  for i in sorting:
    embed.add_field(name=f"***Juara {number}***", value=f"**{i}**")
    number += 1
  await channel.send(embed=embed)
  room.pop(game.get_room_id(), None)

async def player_playing(game, player_now, infonya, chat, channal):
  jalannya = game.dice(player_now)
  game.update_turns()
  await infonya.delete()
  info2 = await channal.send(f"> `{player_now.player_name} {jalannya} Steps forward`")
  await asyncio.sleep(1)
  await chat.delete()
  for i in range(jalannya):
    player_now.update_position(1)

    # City 3
    if player_now.position == 3:
      screenss = await Screen(game, player_now=player_now)
      chat2 = await render_map(channal, screenss, game)
      await info2.delete()
      info2 = await channal.send(f"> `{player_now.player_name} Arrived at Sukasuka City`")
      await asyncio.sleep(5)
      player_now.gacha_skill()
      await skill_want_to_activate(player_now, info2, game, channal)
      await chat2.delete()

  if player_now.position >= 8 and player_now.position <= 39:
    player_now.gacha_skill()
    await skill_want_to_activate(player_now, info2, game, channal)

  await info2.edit(content=f"> `{player_now.player_name} {jalannya} Steps forward`")

  # Win Condition
  if player_now.position > 39:
    game.game_stop()
    player_now.position = 40
    await info2.delete()
    await win_won(game, player_now, channal)
    return

  screenss = await Screen(game, player_now=player_now)
  chat = await render_map(channal, screenss, game)
  return chat, info2

async def play_game(game):
  channel = client.get_channel(game.get_room_id())
  screenss = await Screen(game)
  if not game.game_state():
    await channel.send("Game Over")
    return

  chat = await render_map(channel, screenss, game)
  await reakt(chat)
  infonya = await channel.send("> ***`GAME START`***")

  def check(reaction, user):
    if user.id == player_now.player_id and reaction.message.id == chat.id:
      if str(reaction.emoji) == "🎲" or str(reaction.emoji) == "❌" or str(reaction.emoji) in no_reakt:
        return True

  while game.game_state():
    try:
      players = game.list_player()
      turn = game.get_turns()
      player_now = players[turn]
      reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
    except asyncio.TimeoutError:
      await chat.clear_reactions()
      game.game_stop()
      room.pop(game.get_room_id(), None)
    else:
      channal = reaction.message.channel
      if str(reaction.emoji) == "🎲":  # dice
        chat, infonya = await player_playing(game, player_now, infonya, chat, channal)
        if game.game_state():
          await reakt(chat)

      elif str(reaction.emoji) == no_reakt[0]:  # 0
        await chat.delete()
        screenss = await Screen(game, player_now)
        chat = await render_map(channal, screenss, game)
        await reakt(chat)

      elif str(reaction.emoji) == no_reakt[1]:  # 1
        await chat.delete()
        screenss = await Screen(game, player_now)
        screenss2 = await zooms(screenss, no=1)
        chat = await render_map(channal, screenss2, game)
        await reakt(chat)

      elif str(reaction.emoji) == no_reakt[2]:  # 2
        await chat.delete()
        screenss = await Screen(game, player_now)
        screenss2 = await zooms(screenss, no=2)
        chat = await render_map(channal, screenss2, game)
        await reakt(chat)

      elif str(reaction.emoji) == no_reakt[3]:  # 3
        await chat.delete()
        screenss = await Screen(game, player_now)
        screenss2 = await zooms(screenss, no=3)
        chat = await render_map(channal, screenss2, game)
        await reakt(chat)

      elif str(reaction.emoji) == no_reakt[4]:  # 4
        await chat.delete()
        screenss = await Screen(game, player_now)
        screenss2 = await zooms(screenss, no=4)
        chat = await render_map(channal, screenss2, game)
        await reakt(chat)

      elif str(reaction.emoji) == "❌":
        await chat.edit(content="Game Over", embed=None)
        await chat.clear_reactions()
        game.game_stop()
        room.pop(game.get_room_id(), None)

async def room_game(game):
  channel = client.get_channel(game.get_room_id())

  embed = discord.Embed(
    title="**Join to the Game**",
    color=discord.Colour(0x3498db),
    description="🐍")
  embed.add_field(name=f"**Room** **{channel.name}**", value=" 🎮 = `Join`\n ▶️ = `Play`\n ❌ = `Exit`", inline=False)
  in_room = await channel.send(embed=embed)
  await in_room.add_reaction("🎮") # Join
  await in_room.add_reaction("▶️")  # Play
  await in_room.add_reaction("❌") # Exit

  def check(reaction, user):
    if user.id != my_id and reaction.message.id == in_room.id:
      if str(reaction.emoji) == "▶️" or str(reaction.emoji) == "❌" or str(reaction.emoji) == "🎮":
        return True

  async def cek2(game, user, channel):
    if game.list_player():
      tempss = []
      for pl in game.list_player():
        tempss.append(pl.player_id)
      if user.player_id not in tempss:
        game.join(user)
        await channel.send(f"> `{user.player_name} Joined the Game`")
    else:
      game.join(user)
      await channel.send(f"> `{user.player_name} Joined the Game`")

  while True:
    try:
      reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
    except asyncio.TimeoutError:
      await in_room.clear_reactions()
      room.pop(game.get_room_id(), None)
      break
    else:
      if str(reaction.emoji) == "▶️": # Play
        if len(game.list_player()) < 1:
          await in_room.edit(content="No one in the room :(", embed=None)
          await in_room.clear_reactions()
          break
        game.game_start()
        await in_room.delete()
        await play_game(game)
        break
      if str(reaction.emoji) == "❌":  # Exit
        await in_room.delete()
        room.pop(game.get_room_id(), None)
        break
      if str(reaction.emoji) == "🎮":  # Join
        userss = Player(user, game.get_room_id())
        await cek2(game, userss, channel)

@client.group()
async def snl(ctx):
  if ctx.invoked_subcommand is None:
    embed = discord.Embed(
      title="🐍 **Snake and Ladder**",
      color=discord.Colour(0x3498db),
      timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=ctx.guild.name)
    embed.add_field(name="***Menu***", value=" ⚔️ = `Play`\n ❌ = `Exit`", inline=False)
    chat = await ctx.send(embed=embed)
    await chat.add_reaction("⚔️")
    await chat.add_reaction("❌")

    channel = chat.channel
    chans = channel.id
    if chans in room.keys():
      await chat.edit(content="> `There is already room here, wait for it to finish or reset it`", embed=None)
      await chat.clear_reactions()
    else:
      def check(reaction, user):
        if user == ctx.message.author and reaction.message.id == chat.id:
          if str(reaction.emoji) == "⚔️" or str(reaction.emoji) == "❌":
            return True

      while True:
        try:
          reaction, user = await client.wait_for("reaction_add", timeout=120, check=check)
        except asyncio.TimeoutError:
          await chat.clear_reactions()
          break
        else:
          if str(reaction.emoji) == "⚔️":
            room[channel.id] = channel.id
            game = GameSnL(channel.id)
            await chat.delete()
            await room_game(game)
            break
          elif str(reaction.emoji) == "❌":
            await chat.delete()
            break





@client.command()
async def howgay(ctx, member: discord.Member = None):
        member = member or ctx.author
        response=[random.randint(0,100)]
        embed=discord.Embed(title='Gay Rating Device!',
        description=f"\n{member.mention} is {random.choice(response)}% gay!!  :rainbow_flag:",color  = 0xdb7bff)
        await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.add_field(name="<a:pepelaughboom:826519617840873523> - : Fun Commands", value="All my fun Commands!```f!snl\nf!howgay\nf!cry\nf!smile\nf!rickroll\nf!tod\nf!reset(only in the snakes and ladders game.)\nf!coinflip\nf!say\nf!gsm\nf!pat\nf!cool\nf!howpp\nf!avatar\nf!editsnipe\nf!snipe```", inline=False)
    embed.add_field(name=" <a:GunBoi:826519850096132161> - : Moderation", value="All my moderation Commands!```f!ban\nf!kick\nf!mute\nf!unban\nf!unmute```", inline=False)
    embed.add_field(name=" <:question:826519991381786678> - : Info", value="All my information Commands!```f!creator\nf!ping\nf!poll```", inline=False)
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction("✅")

@client.command(alaises=['Cry','Cri','Sad'])
async def cry(ctx):
      embed= discord.Embed(title=f'{ctx.author.name} is crying :sob: , My heart is gonna break!! :broken_heart:  ',
      color=0xdb7bff)
      gifs=['https://media1.tenor.com/images/8f6da405119d24f7f86ff036d02c2fd4/tenor.gif?itemid=5378935',
      'https://media1.tenor.com/images/3b1a145fc182fd2b0cbb29d32e37f43b/tenor.gif?itemid=8572836',
      'https://media1.tenor.com/images/e07ff7159c902150890d84329d253931/tenor.gif?itemid=15021750',
      'https://media1.tenor.com/images/67df1dca3260e0032f40048759a967a5/tenor.gif?itemid=5415917',
      'https://media1.tenor.com/images/213ec50caaf02d27d358363016204d1d/tenor.gif?itemid=4553386',
      'https://media1.tenor.com/images/bdd8e3865332d5ccf2edddd1460e0792/tenor.gif?itemid=16786822',
      'https://media1.tenor.com/images/bc6517ddc10fc60c4dc73c9e3a00eafa/tenor.gif?itemid=13995463]',
      'https://tenor.com/view/oh-no-sad-cry-crying-yui-hirasawa-gif-5415917',
      'https://media.tenor.com/images/224221bb396c782daa0333a23a1c4d51/tenor.gif']
      link= random.choice(gifs)
      embed.set_image(url=f'{link}')
      await ctx.send(embed=embed)

@client.command(alaises=['Smile','Happy','Grin'])
async def smile(ctx):
      embed= discord.Embed(title=f'{ctx.author.name} smiles! :grin:  ',
      color=0xdb7bff)
      gifs=['https://cdn.discordapp.com/attachments/697029214289002539/720796063950176286/image0.gif',
      'https://cdn.discordapp.com/attachments/697029214289002539/720796063950176286/image0.gif',
      'https://images-ext-1.discordapp.net/external/Qj9mj2E1YDcVTespi0Vfig-RiaAc7N0uy88Q0IahBng/https://cdn.weeb.sh/images/rkH84ytPZ.gif?width=400&height=225',
      'https://media.discordapp.net/attachments/697029214289002539/721016708776722574/image0.gif',
      'https://cdn.discordapp.com/attachments/719560200897691728/721351702808363008/image0.gif',
      'http://pa1.narvii.com/6339/ad70e90381a8a5bf9b59657feb86e0bc34108b59_hq.gif?size=450x320']
      link= random.choice(gifs)
      embed.set_image(url=f'{link}')
      await ctx.send(embed=embed)

@client.command(alaises=['rick'])
async def rickroll(ctx):
    embed= discord.Embed(title=f'{ctx.author.name} Got rickrolled',
        color=0xdb7bff)
    gifs=['https://media.tenor.com/images/a5d46f7b746bf96c8a70b7f5a788e201/tenor.gif']
    link= random.choice(gifs)
    embed.set_image(url=f'{link}')
    await ctx.send(embed=embed)

@client.command()
async def tod(ctx):
  Truth_or_dares = ["Truth: **What is your real name?**", "Truth: **What is your age?**", "Truth: **Are you still a minor?**", "Truth: **What does your Parents do?**", "Truth: **How will you react if your friends hated you?**", "Truth: **Who is your best friend name? Virtual name is fine**", "Truth: **Do you have any friends that hate you?**", "Truth: **Who are you Simping for?**", "Truth: **Have you ever commited any crime?**", "Truth: **What you have planned for your future?**", "Truth: **Do you have any Girlfriend?**", "Truth: **Are you a simp?**", "Truth: **What is your Childhood nightmare?**", "Truth: **What will you do with your Homework?**", "Truth: **What did you eat for lunch?**", "Truth: **Do you hate Reading?**", "Truth: **What movie do you like?**", "Truth: **Where do you live?**", "Truth: **How many Languages you know?**", "Truth: **What is your favorite Meme?**", "Truth: **Do you hate Light theme? (in Websites)**", "Truth: **What Music you like?**", "Truth: **Are you choosen by the no name cult song?**", "Truth: **Do you like your Girlfriend?**", "Truth: **What will you do if you have all the wealth in the world?**", "Truth: **What will you do if you get bullied by your best friend?**", "Truth: **Do you have a dog?**", "Truth: **Do you have a cat?**", "Dare: **Dance on the road for 30 seconds**", "Dare: **Eat a cheeseburger**", "Dare: **Simp for someone**", "Dare: **Water your flowers with Water**", "Dare: **Find your cat or your dog and pat them**", "Dare: **Be an Uwu People**", "Dare: **Say anything with the UwU language for 30 Minutes**", "Dare: **Drink 50 Water bottle in 1 Minute**", "Dare: **Cook and ate anything in the fridge**", "Dare: **Learn until you understand all of it**", "Dare: **Read a 600 Page book**", "Dare: **Make Mac'n Cheese**", "Dare: **Simp to People for 1 hour**", "Dare: **Use an Anime cute Loli Avatar on your Social Application**", "Dare: **Send feet pics to your friend**"]
  todembed = discord.Embed(description=(random.choice(Truth_or_dares)), colour = discord.Colour.blurple())
  todembed.set_footer(text=f'If you dont wanna do an truth or dare you dont have to!', icon_url=f'{ctx.guild.icon_url}')
  todembed.set_author(name=f'Requested by {ctx.author}', icon_url=f'{ctx.author.avatar_url}')
  await ctx.send(embed=todembed)

@client.command(aliases=["Ban", "BAN"])
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, reason=None):
  """Bans a user"""
  if reason == None:
      messageok = f"You have been banned from {ctx.guild.name} for: ``{reason}``"
      await member.send(messageok)
      await member.ban(reason=reason)

      em1 = embed=discord.Embed(title="✅ Member Banned.", colour=0xff0000)
      msg = await ctx.send(embed=em1)
      await msg.edit(embed=em1)
      em2 = embed=discord.Embed(title="✅ Member Banned.", colour=0x77ff00)
      await msg.edit(embed=em2)
      em3 = embed=discord.Embed(title="✅ Member Banned.", colour=0xffaa00)
      await msg.edit(embed=em3)
      em4 = embed=discord.Embed(title="✅ Member Banned.", colour=0x00ddff)
      await msg.edit(embed=em4)
      em5 = embed=discord.Embed(title="✅ Member Banned.", colour=0x0033ff)
      await msg.edit(embed=em5)
      em6 = embed=discord.Embed(title="✅ Member Banned.", colour=0xff00dd)
      await msg.edit(embed=em6)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
      embed=discord.Embed()
      embed.title="Missing Permissions."
      embed.description=f"You Do Not Have **Permissions** To Ban This Member."
      embed.color=0xff0000
      await ctx.send(embed=embed)

@client.command()
async def kick(ctx, user:discord.User):
    await ctx.guild.ban(user)
    await asyncio.sleep(1)
    await ctx.guild.unban(user)
    em1 = embed=discord.Embed(title="✅ Member Kicked.", colour=0xff0000)
    msg = await ctx.send(embed=em1)
    await msg.edit(embed=em1)
    em2 = embed=discord.Embed(title="✅ Member Kicked.", colour=0x77ff00)
    await msg.edit(embed=em2)
    em3 = embed=discord.Embed(title="✅ Member Kicked.", colour=0xffaa00)
    await msg.edit(embed=em3)
    em4 = embed=discord.Embed(title="✅ Member Kicked.", colour=0x00ddff)
    await msg.edit(embed=em4)
    em5 = embed=discord.Embed(title="✅ Member Kicked.", colour=0x0033ff)
    await msg.edit(embed=em5)
    em6 = embed=discord.Embed(title="✅ Member Kicked.", colour=0xff00dd)
    await msg.edit(embed=em6)
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
      embed=discord.Embed()
      embed.title="Missing Permissions."
      embed.description=f"You Do Not Have **Permissions** To kick This Member."
      embed.color=0xff0000
      await ctx.send(embed=embed)


@client.command(name='logout', aliases=['shutdown'])
@commands.is_owner()
async def botstop(ctx):
  await ctx.send('Shutting down for updates :wave:')
  await client.logout()


@client.command()
async def reset(ctx):
  channel = ctx.message.channel.id
  room.pop(channel, None)
  await ctx.send("Room has been reset")


@client.command()
async def credits(ctx):
  await ctx.send('**[CREDITS]: Made by Purge#1338**')
  await ctx.message.add_reaction("✅")


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None):
  if not member:
    await ctx.send("Please specify a member")
    return
  role = discord.utils.get(ctx.guild.roles, name="muted")
  await member.add_roles(role)
  await ctx.send(" `` Muted an insect `` ")


@client.command(pass_context=True)
async def ping(ctx):
    ping_in_millis = round((client.latency * 1000), 4)
    await ctx.channel.send(f'Your ping is {str(ping_in_millis) } ms!')




@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if(user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send("Unbanned someone")
      return

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
  if not member:
    await ctx.send("Please specify a member")
    return
  role = discord.utils.get(ctx.guild.roles, name="muted")
  await member.remove_roles(role)
  await ctx.send("``unmuted someone``")

@client.command(aliases = ['pl'])
async def poll(ctx,*, msg):
  channel = ctx.channel
  try:
    op1 , op2 = msg.split("or")
    txt = f"React with ✅ for {op1} or ❎ for {op2}" 
  except:
    await channel.send("Please make it like this: [Choice1] or [Choice2]")
    return



  embed = discord.Embed(title="Poll", description = txt,colour = discord.Colour.red())
  message_ = await channel.send(embed=embed)
  #message_ = await ctx.send("React here ")
  await message_.add_reaction("✅")
  await message_.add_reaction("❎")
  await ctx.message.delete()

  await asyncio.sleep(10)
  cache_msg = await ctx.fetch_message(message_.id)
  rs = cache_msg.reactions

  users1 = await rs[0].users().flatten()
  users2 = await rs[1].users().flatten()
  op1p = len(users1)
  op2p = len(users2)

  if op1p > op2p:
    await ctx.send(op1+ " has won!")
  elif op1p < op2p:
    await ctx.send(op2+ " has won!")
  else:
    await ctx.send("It's a tie!")


@client.command(pass_context=True)
async def coinflip(ctx):
  choices = ["🪙 Heads", "🪙 Tails"]
  ranchoice = random.choice(choices)
  await ctx.send(ranchoice)

@client.command(pass_context = True)
async def say(ctx, *,msg):
  await ctx.message.delete()
  await ctx.send(msg)

@client.command(pass_context=True)
async def pat(ctx, member : discord.Member ):
  embed = discord.Embed(title= f" {Bot_name} gave pats to {member}",color=0xFF69B4)
  embed.set_image(url="https://i.imgur.com/2lacG7l.gif")
  await ctx.send(embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def gsm(ctx, *,msg):
  await ctx.message.delete()
  embed = discord.Embed(title="<a:aItemMega:826516642535702558> Global System Message", description=msg)
  await ctx.send(embed=embed)

@client.command()
async def cool(ctx):
  embed = discord.Embed(title="Im Cool", description="<a:hehe:826518250669736029> Random Command.")
  await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
  embed = discord.Embed(title = "Thanks for considering!", description = f"[Click Here](https://discord.com/api/oauth2/authorize?client_id=825972660554170368&permissions=8&scope=bot) to invite me to your server! \n Currently, I'm in {len(client.guilds)} servers!", color = discord.Color.green())
  embed.set_footer(text = f"[Support Server]https://discord.gg/CMAT3ZZvzX", icon_url = client.user.avatar_url)
  await ctx.send(embed = embed)

@client.command()
async def howpp(ctx, member: discord.Member = None):
        member = member or ctx.author
        response=['8=======D','8==D', '8===D','8====D', '8====D', '8=========D','8D', '8=D']
        embed=discord.Embed(title='How long is the pp?',
        description=f"\n{member.mention} pp is {random.choice(response)}",color  = 0x206694)
        await ctx.send(embed=embed)


@client.command(name='avatar')
async def avatar(ctx, member: discord.Member=None):
    try:
        await ctx.send('{}'.format(member.avatar_url))
    except: 
        await ctx.send('{}'.format(ctx.message.author.avatar_url))


@client.command(name = 'editsnipe')
async def editsnipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Edited Message #{channel.name}", description = editsnipe_message_content[channel.id], color=0xfdefef)
        em.set_footer(text = str("Today At:" + editsnipe_message_time[channel.id]))
        em.set_author(name=editsnipe_message_author[channel.id], icon_url=editsnipe_message_pfp[channel.id])
        await ctx.send(embed = em)
    except:
        await ctx.send(f"There are no recently edited messages in #{channel.name}")

@client.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Sniped Message #{channel.name}", description = snipe_message_content[channel.id], color=0xfdefef)
        em.set_footer(text = str("Today At:" + snipe_message_time[channel.id]))
        em.set_author(name=snipe_message_author[channel.id], icon_url=snipe_message_pfp[channel.id])
        await ctx.send(embed = em)
    except:
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")
        
@client.command(aliases=["aki"])
async def akinator(ctx):
    async with ctx.typing():
        intro = discord.Embed(title="Akinator", description="Hello, " + ctx.author.mention + "I am Akinator!!!",
                              color=discord.Colour.blue())
        intro.set_thumbnail(url="https://en.akinator.com/bundles/elokencesite/images/akinator.png?v93")
        intro.set_footer(text="Think about a real or fictional character. I will try to guess who it is")
        bye = discord.Embed(title="Akinator", description="Bye, " + ctx.author.mention, color=discord.Colour.blue())
        bye.set_footer(text="Akinator left the chat!!")
        bye.set_thumbnail(url="https://i.pinimg.com/originals/28/fc/0b/28fc0b88d8ded3bb8f89cb23b3e9aa7b.png")
        await ctx.send(embed=intro)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n", "p",
                                                                                                       "b",
                                                                                                       "yes", "no",
                                                                                                       "probably",
                                                                                                       "idk",
                                                                                                       "back"]

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                question = discord.Embed(title="Question", description=q, color=discord.Colour.blue())
                ques = ["https://i.imgflip.com/uojn8.jpg",
                        "https://ih1.redbubble.net/image.297680471.0027/flat,750x1000,075,f.u1.jpg"]
                question.set_thumbnail(url=ques[random.randint(0, 1)])
                question.set_footer(text="Your answer:(y/n/p/idk/b)")
                question_sent = await ctx.send(embed=question)
                try:
                    msg = await client.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    # await question_sent.delete()
                    await ctx.send("Sorry you took too long to respond!(waited for 30sec)")
                    await ctx.send(embed=bye)
                    return
                # await question_sent.delete()
                if msg.content.lower() in ["b", "back"]:
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()
            answer = discord.Embed(title=aki.first_guess['name'], description=aki.first_guess['description'],
                                   color=discord.Colour.blue())
            answer.set_thumbnail(url=aki.first_guess['absolute_picture_path'])
            answer.set_image(url=aki.first_guess['absolute_picture_path'])
            answer.set_footer(text="Was I correct?(y/n)")
            await ctx.send(embed=answer)
            # await ctx.send(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?(y/n)\n{aki.first_guess['absolute_picture_path']}\n\t")
            try:
                correct = await client.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("Sorry you took too long to respond!(waited for 30sec)")
                await ctx.send(embed=bye)
                return
            if correct.content.lower() == "y":
                yes = discord.Embed(title="Yeah!!!", color=discord.Colour.blue())
                yes.set_thumbnail(url="https://i.pinimg.com/originals/ae/aa/d7/aeaad720bd3c42b095c9a6788ac2df9a.png")
                await ctx.send(embed=yes)
            else:
                no = discord.Embed(title="Oh Noooooo!!!", color=discord.Colour.blue())
                no.set_thumbnail(url="https://i.pinimg.com/originals/0a/8c/12/0a8c1218eeaadf5cfe90140e32558e64.png")
                await ctx.send(embed=no)
            await ctx.send(embed=bye)
        except Exception as e:
            await ctx.send(e)

client.run(token)
