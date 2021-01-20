import discord
import os
from discord.ext import commands

from cogs.Utility import *

class Misc(commands.Cog):
		
	def __init__(self, client):
		self.client = client
			
	@commands.Cog.listener()
	async def on_ready(self):
		pull_ratings()
		pull_games()
		print('Bot is ready')
		
	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def ping(self, ctx):
		'''
		Sends "Pong!"
		'''
		await ctx.send('Pong!')
		
	@commands.command()
	@commands.cooldown(1, 15, commands.BucketType.default)
	async def update(self, ctx):
		'''
		Compiles the latest version of Beat Jamin
		Compile message of 1 means that there were compile errors
		Compiler: g++
		'''
		#os.system('echo hi')
		compile_cmd = 'g++ '
		for filename in os.listdir('engine'):
			#os.system(f'echo {filename}')
			#print(filename, filename[-4:], filename[-2:])
			if filename[-4:] == '.cpp' or filename[-2:] == '.h':
				compile_cmd += f'engine/{filename} '
		compile_cmd += '-o jamin'
		#os.system(f'echo {compile_cmd}')
		out = os.system(compile_cmd)
		
		await ctx.send(f'Updated\nCompile Message: {out}')

	@commands.command()
	@commands.cooldown(1, 3, commands.BucketType.default)
	async def rating(self, ctx):
		'''
		Tells you your rating
		'''
		await ctx.send(f'Your rating is {get_rating(ctx.message.author.id)}')

	@commands.command()
	@commands.cooldown(1, 4, commands.BucketType.default)
	async def botinfo(self, ctx):
		embed=discord.Embed(title="Bot Info", color=0xff0000)
		embed.add_field(name="Links", 
			value="[https://github.com/jeffarjeffar/Jamin_Bot_bruh](Github) | [https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=1610088278&scope=bot](Invite)",
			inline=True)
		embed.add_field(name="Info",
			value='Chess Bot is a bot that plays chess.')
		embed.set_footer(text="Made by Farmer John#3907")
		await ctx.send(embed=embed)


