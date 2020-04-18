# Author : TK
# Rev 1.0 for grinding notification purposes
# 
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import pandas as pd
DISCORD_TOKEN={'NzAwNjY4ODQ1NTA5MzEyNTQy.XpmTgg.W_RlsTDPTURPHYDnEToWvgv6V3o'}
# DISCORD_GUILD={'your-guild-name'}
load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = 'NzAwNjY4ODQ1NTA5MzEyNTQy.XpqV0A.71leMalbjig4D3B11K2ZlJGZZn8'
GUILD = 'tkhouse'


client = discord.Client()
bot = commands.Bot(command_prefix='!')

bot.grinding_list = pd.DataFrame(columns=["Player","GrindingSpot","Channel","Time","Expiry"])
from datetime import datetime,timedelta
now = datetime.now()

@bot.event
async def on_ready():
    print("Meow is ready to rock and roll!")

@bot.command(name='reg', help='Option for grinding spot.')
async def reg(ctx, place: str , channel: str , minutes: str):
    message_register = """"Registered entry {author}  {place}-{channel} @ {time} """.format(author=str(ctx.author),place=place,channel=channel,time= now.strftime("%d/%m/%Y %H:%M:%S"))
    expiry_time = datetime.now() + timedelta(minutes=int(minutes))
    current_df = {"Player":str(ctx.author),"GrindingSpot":place,"Channel":channel,"Time":now,"Expiry":expiry_time,"LuckyCat":"No Meow"}
    bot.grinding_list = bot.grinding_list.append(current_df,ignore_index=True)
    print(bot.grinding_list)
    await ctx.send(message_register)
    await ctx.send("Please bring TK fly , he will shout 666!!",)


@bot.command(name='pick', help='Pick up a grinding spot')
async def pick(ctx, index:int):
    if bot.grinding_list.loc[index,'LuckyCat'] != "No Meow":
        message_failed = "Sorry ...it was taken by {} ".format(bot.grinding_list.loc[index,'LuckyCat'])
        await ctx.send(message_failed)
    else:
        bot.grinding_list.loc[index,'LuckyCat'] = str(ctx.author)
        message_success = "Congratulations!! You should bring {} to fly high high later".format(bot.grinding_list.loc[index,'Player'])
        await ctx.send(message_success)

# Create finding spot command
@bot.command(name="gspot",help="Getting a list of available grind spot")
async def gspot(ctx):
    # Filter list will be refresh to make sure all the list came out is before expiry
    bot.grinding_list = bot.grinding_list[bot.grinding_list['Expiry'] > datetime.now()]
    for idx,data in bot.grinding_list.iterrows():
        print(idx)
        embed = discord.Embed(
        title='Grinding Spot',
        description = 'Grinding spot available',
        color = discord.Colour.blue()
        )
        embed.add_field(name='Index',value=idx,inline=False)
        for id,dt in data.items():
            embed.add_field(name=id,value=dt,inline=False)

        await ctx.send(embed=embed)


bot.run(TOKEN)
