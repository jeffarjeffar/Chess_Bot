import discord
import os
import subprocess
from discord.ext import commands
import random
import asyncio

from cogs.Utility import *


thonking = []


class Beat_Jamin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['play'])
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def move(self, ctx, move):
        '''
        Plays <move> against the computer
        Please enter the move in algebraic notation
        For example, Nxe4, Nge5, c4, Ke2, etc
        '''
        if not ctx.author.id in games.keys():
            await ctx.send('You do not have a game in progress with Chess Bot')
            return

        if ctx.author.id in thonking:
            await ctx.send('Chess Bot is already thinking')
            return

        if len(thonking) > 3:
            await ctx.send('Resources overloaded. Please wait...')
            while len(thonking) > 3:
                await asyncio.sleep(5)

        person = ctx.author.id
        thonking.append(person)
        file_in = f'data/input-{person}.txt'
        file_out = f'data/output-{person}.txt'
        if not file_in[5:] in os.listdir('data'):
            f = open(file_in, 'x')
            f.close()
        if not file_out[5:] in os.listdir('data'):
            f = open(file_out, 'x')
            f.close()

        f = open(file_in, 'w')
        f.write('play\n')
        if len(games[ctx.author.id]) == 0:
            f.write('no\n')
        else:
            f.write('yes2\n')
            game_str = ''
            for i in range(len(games[ctx.author.id])):
                if i % 2 == 0:
                    game_str += str(i//2+1) + '. '
                game_str += str(games[ctx.author.id][i]) + ' '
            game_str += '*'
            f.write(game_str + '\n')
        f.write(f'{time_control[ctx.author.id]}\n')
        if colors[ctx.author.id] == 0:
            f.write('white\n')
        else:
            f.write('black\n')
        f.write(move + '\nquit\nquit\n')
        f.close()
        await ctx.send('Chess Bot is thinking...')
        subprocess.call(['./a'], stdin=open(file_in),
                        stdout=open(file_out, 'w'))
        f = open(file_out)
        out = f.readlines()
        f.close()
        if out[-3] != 'GAME STILL IN PROGRESS\n':
            thonking.remove(person)
            # print(out[-3])
            if out[-3] == 'ILLEGAL MOVE PLAYED\n':
                await ctx.send('Haha, nice try')
                return
            if out[-3] == 'COMPUTER RESIGNED\n':
                await ctx.send('Chess Bot resigned')
                update_rating(ctx.author.id, 1)
                await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
                games.pop(ctx.author.id)
                push_games()
                return

            winner = 0
            if out[-3] == 'DRAW\n':
                update_rating(ctx.author.id, 1/2)
                await ctx.send('Draw')
            else:
                if out[-3] == 'WHITE WON\n':
                    winner = 1
                if winner == colors[ctx.author.id]:
                    update_rating(ctx.author.id, 1)
                    await ctx.send('You won!')
                else:
                    update_rating(ctx.author.id, 0)
                    await ctx.send('You lost.')

            await ctx.send(f'Your new rating is {get_rating(ctx.author.id)}')
            games.pop(ctx.author.id)
            push_games()
            return
        move = int(out[-24][31:-2])
        await ctx.send(f'<@{person}>')
        await ctx.send(out[-24])
        # await ctx.send(out[-23])
        msg1 = '```\n'
        for i in range(-21, -4, 2):
            #os.system(f'echo {i}')
            msg1 += out[i] + '\n'
            #os.system(f'echo "{msg1}"')
        msg1 += '```'
        await ctx.send(msg1)
        game_str = out[-2][:-1].split(' ')
        games[ctx.message.author.id].clear()
        for i in game_str:
            if i == '' or i == '\n':
                continue
            games[ctx.message.author.id].append(int(i))
            #os.system(f'echo {i}')
        push_games()
        thonking.remove(person)

        log_channel = self.client.get_channel(798277701210341459)
        msg = f'<{person}>\n```\n'
        for i in range(len(out)):
            msg += out[i] + '\n'
            if i % 10 == 0:
                msg += '```'
                await log_channel.send(msg)
                msg = '```'
        msg += '```'
        await log_channel.send(msg)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def challenge(self, ctx, *flags):
        '''
        Challenges Chess Bot to a game
                Your color is assigned randomly.
                Flags:
                -t to set time control (in seconds)
        '''
        if ctx.author.id in games.keys():
            await ctx.send('You already have a game in progress')
            return

        time_control[ctx.author.id] = 60

        for i in range(0, len(flags), 2):
            os.system(f'echo {flags[i]}')
            if flags[i] == '-t':
                time_control[ctx.author.id] = int(flags[i+1])

        games[ctx.author.id] = []
        colors[ctx.author.id] = random.randint(0, 1)  # 1 if white, 0 if black

        await ctx.send('Game started with Chess Bot')
        if colors[ctx.author.id] == 0:
            await ctx.send('You are black')
        else:
            await ctx.send('You are white')

        if colors[ctx.author.id] == 0:
            person = ctx.author.id
            file_in = f'data/input-{person}.txt'
            file_out = f'data/output-{person}.txt'
            if not file_in[5:] in os.listdir('data'):
                f = open(file_in, 'x')
                f.close()
            if not file_out[5:] in os.listdir('data'):
                f = open(file_out, 'x')
                f.close()

            f = open(file_in, 'w')
            f.write(
                f'play\nno\n{time_control[ctx.author.id]}\nwhite\nquit\nquit')
            f.close()
            #print('Starting a')

            subprocess.call(['./a'], stdin=open(file_in),
                            stdout=open(file_out, 'w'))
            f = open(file_out)
            out = f.readlines()
            move = int(out[-24][31:-2])
            await ctx.send(out[-24])
            await ctx.send(out[-23])
            msg1 = '```\n'
            for i in range(-21, -6, 2):
                #os.system(f'echo {i}')
                msg1 += out[i] + '\n'
                #os.system(f'echo "{msg1}"')
            msg1 += '```'
            await ctx.send(msg1)
            await ctx.send(out[-5])
            game_str = out[-2].split(' ')
            games[ctx.author.id].clear()
            for i in game_str:
                if i == '' or i == '\n':
                    continue
                games[ctx.author.id].append(int(i))
            push_games()

            log_channel = self.client.get_channel(798277701210341459)
            msg = '```\n'
            for i in range(len(out)):
                msg += out[i] + '\n'
                if i % 10 == 0:
                    msg += '```'
                    await log_channel.send(msg)
                    msg = '```'
            msg += '```'
            await log_channel.send(msg)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.default)
    async def abort(self, ctx, user):
        '''
        Aborts a game
        '''
        if not is_mooderator(ctx.author):
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
    async def resign(self, ctx):
        '''
        Resigns the game
        '''
        if not ctx.author.id in games.keys():
            await ctx.send('You do not have a game in progress')
            return

        games.pop(ctx.message.author.id)
        update_rating(ctx.author.id, 0)
        await ctx.send(f'Game resigned. Your new rating is {get_rating(ctx.author.id)}')
        push_games()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def view(self, ctx, *user):
        '''
        Views your current game
        '''

        person = -1
        if len(user) == 1:
            person = int(user[0][3:-1])
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

        person = ctx.author.id
        file_in = f'data/input-{person}.txt'
        file_out = f'data/output-{person}.txt'
        # for asdf in os.listdir('data'):
        #	os.system(f'echo {asdf}')
        #os.system(f'echo {file_in[5:]}')
        if not file_in[5:] in os.listdir('data'):
            f = open(file_in, 'x')
            f.close()
        if not file_out[5:] in os.listdir('data'):
            f = open(file_out, 'x')
            f.close()

        f = open(file_in, 'w')
        f.write('play\n')
        if len(games[person]) == 0:
            f.write('no\n')
        else:
            f.write('yes2\n')
            game_str = ''
            for i in range(len(games[person])):
                if i % 2 == 0:
                    game_str += str(i//2+1) + '. '
                game_str += str(games[person][i]) + ' '
            game_str += '*'
            f.write(game_str + '\n')
        f.write('60\n')
        if colors[person] == 0:
            f.write('white\n')
        else:
            f.write('black\n')
        f.write('\nquit\nquit\n')
        f.close()
        subprocess.call(['./a'], stdin=open(file_in),
                        stdout=open(file_out, 'w'))
        f = open(file_out)
        out = f.readlines()
        f.close()
        game = f'<@{ctx.author.id}>\n```\n'
        for i in range(-20, -4, 2):
            #os.system(f'echo {i}')
            game += out[i] + '\n'
            #os.system(f'echo "{msg1}"')
        game += '```'
        await ctx.send(game)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def fen(self, ctx, *user):
        '''
        Sends current game in FEN format
        '''

        person = -1
        if len(user) == 1:
            person = int(user[0][3:-1])
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

        person = ctx.author.id
        file_in = f'data/input-{person}.txt'
        file_out = f'data/output-{person}.txt'
        # for asdf in os.listdir('data'):
        #	os.system(f'echo {asdf}')
        #os.system(f'echo {file_in[5:]}')
        if not file_in[5:] in os.listdir('data'):
            f = open(file_in, 'x')
            f.close()
        if not file_out[5:] in os.listdir('data'):
            f = open(file_out, 'x')
            f.close()

        f = open(file_in, 'w')
        f.write('fen\n')
        if len(games[person]) == 0:
            f.write('no\n')
        else:
            f.write('yes2\n')
            game_str = ''
            for i in range(len(games[person])):
                if i % 2 == 0:
                    game_str += str(i//2+1) + '. '
                game_str += str(games[person][i]) + ' '
            game_str += '*'
            f.write(game_str + '\n')
        f.write('quit\n')
        f.close()
        subprocess.call(['./a'], stdin=open(file_in),
                        stdout=open(file_out, 'w'))
        f = open(file_out)
        out = f.readlines()
        f.close()

        await ctx.send(out[-2])
