import mysql.connector
import discord
import os
from discord.ext import commands
import vars
from discord import File
import discord.utils
from PIL import Image, ImageDraw, ImageFont
import io

client = commands.Bot(command_prefix='=', case_insensitive=True)

config = {
  'user': vars.u1882538_vis85wBDGC,
  'password': vars.2!FeBl!iKaM0oZCH+Z!g=smo,
  'host': vars.5.9.8.124,
  'database': vars.s1882538_my-db1694424146,
  'raise_on_warnings': True
}

def connectdatabase():
  try:
      cnx = mysql.connector.connect(**config)
      cursor = cnx.cursor()
      print("MySQL Connection Created Successfully")
  except Exception as e:
      print(e)
      print("Exitting...")
      exit()

  def exec(query):
      try:
          cursor.execute(query)
          return cursor.fetchall()
      except Exception as e:
          return str(e)


@client.event
async def on_ready():
    print('Bot is running')
    await client.change_presence(activity=discord.Game(name="Remembering Asiania RPG..."))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("You entered an invalid command. Try =help to see list of commands.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit = amount)


@client.command(aliases=['online', 'total'])
async def players(ctx):
    await ctx.send('Horizon Roleplay has been shut down. Thanks for playing.')
    return
    if ctx.channel.id != 1138191176751665182:
      await ctx.send('Wrong channel. Use this command in <#1138191176751665182>.')
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE isonline = '1'"
    cursor.execute(sql)
    total="Name - Level\n"
    substring=""
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("There's no one online.")
      return
    players=0;
    for row in cursor:
        name = row[1]
        level = row[11]
        substring= f'\n{name} - {level}'
        total =  total + substring
        players += 1
    await ctx.send(f'```{total}\n\nTotal: {players} | Asiania RPG | https://axiania.com | 51.79.204.126:7777```')
    cursor.close()
    cnx.close()


@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx, *, name=None):
    if not name:
      await ctx.send("=unban [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM banned WHERE user_name = %s", (name, ))
    deleted_row_count = cursor.rowcount
    if not deleted_row_count:
      await ctx.send("Couldnot find a banned player with that name.")
      return
    cnx.commit()
    await ctx.send("You have successfully unbanned the specified player.")

    cursor.close()
    cnx.close()

@client.command(aliases=['signature', 'sig'])
async def stats(ctx,*, name=None ):
    if not name:
      await ctx.send("=stats [Firstname_LastName]")
      return
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE p_name = %s", (name, ))
    
    myresult = cursor.fetchall()
    if not  myresult:
      await ctx.send("Couldnot find the specified name in the database.")
      return

    bank = 0
    for x in myresult:
      user_id = x[0]
      playername=x[1]
      level=x[11]
      money=x[10]
      hours=x[38]
      lastlogin=x[52]
      skin=x[17]

    cursor.execute("SELECT * FROM bank WHERE bankOwner = %s LIMIT 5", (user_id, ))
    
    for row in cursor:
        bank = bank + row[1]


    SKIN_SIZE = 256
    AVATAR_SIZE = 256
    background_image = Image.open('bg123.png') 
    background_image = background_image.convert('RGBA')
    image = background_image.copy()

    image_width, image_height = image.size



    draw = ImageDraw.Draw(image) 
    text = f'Name: {playername}'
    font = ImageFont.truetype("goodtimes.ttf", 45, encoding="unic")

    text_width, text_height = draw.textsize(text, font=font)


    draw.text((460, 100), text, fill=(255,255,255,255), font=font)
    text = f'Level: {level}'
    draw.text((460, 200), text, fill=(255,255,255,255), font=font)
    text = f'Cash: {money}$'
    draw.text((460, 300), text, fill=(255,255,255,255), font=font)
    text = f'Bank: {bank}$'
    draw.text((460, 400), text, fill=(255,255,255,255), font=font)
    text = f'Hours Played: {hours}'
    draw.text((460, 500), text, fill=(255,255,255,255), font=font)
    text = f'Last Login: {lastlogin}'
    draw.text((460, 600), text, fill=(255,255,255,255), font=font)


    imagelink = f'skins/{skin}.png'
    avatar_image= Image.open(imagelink)
    avatar_image = avatar_image.convert('RGBA')
    avatar_image = avatar_image.resize((350, 800)) 
    image.paste(avatar_image, (0, 0), avatar_image)


    buffer_output = io.BytesIO()
    image.save(buffer_output, format='PNG')
    buffer_output.seek(0)
    await ctx.send(file=File(buffer_output, f'{name}.png'))
    cursor.close()
    cnx.close()

client.run('MTEzMzMzNDk0NjE3ODY2NjUyNg.Gb0ikk.tVnvSnh3h60CJldHyKeQo3uJ6RjkZ1Wwh20hR8')
