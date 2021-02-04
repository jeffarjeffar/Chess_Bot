import discord
from discord.ext import commands

from cogs.Utility import *

class Mooderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def abort(self, ctx, user):
        '''
        Aborts a game
        '''
        
        if not has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Debugger', 'Chess-Admin', 'Chess-Debugger'], self.client):
            await ctx.send('You do not have permission to abort games')
            return

        person = int(user[3:-1])

        if not person in games.keys():
            await ctx.send('You do not have a game in progress')
            return

        games.pop(person)
        await ctx.send('Game aborted')
        push_games()
        
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def refund(self, ctx, user : discord.Member, points : float):
        '''
        Refunds rating points to a user
        '''
        
        if not has_roles(ctx.author.id, ['Admin', 'Mooderator', 'Moderator', 'Chess-Admin'], self.client):
            await ctx.send('You do not have permission to refund rating')
            return

        ratings[user.id] += points
        ratings[801501916810838066] -= points
        
        await ctx.send(f'{points} points refunded')
        push_ratings()