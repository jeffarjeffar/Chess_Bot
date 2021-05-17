import os
import discord
from PIL import Image
import time

import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Utility as util
from Chess_Bot.cogs.Images import *

whiteblack = ['black', 'white']


def prepare_files(person):
    file_in = f'Chess_Bot/data/input-{person}.txt'
    file_out = f'Chess_Bot/data/output-{person}.txt'

    if not file_in[15:] in os.listdir('Chess_Bot/data'):
        f = open(file_in, 'x')
        f.close()
    if not file_out[15:] in os.listdir('Chess_Bot/data'):
        f = open(file_out, 'x')
        f.close()

    return file_in, file_out


def prepare_input(person, move=''):
    file_in = f'Chess_Bot/data/input-{person}.txt'

    game = data.data_manager.get_game(person)

    f = open(file_in, 'w')
    f.write(
        f'play\n{whiteblack[1 - game.color]}\nyes2\n{str(game)}\n{game.time_control}\n{move}\nquit\nquit\n')
    f.close()


async def run_engine(file_in, file_out):
    # print('Running engine')
    out, err, status = await util.run(f'./engine < {file_in} > {file_out}')
    # print(f'Stdout: {out}\nStderr: {err}\n{status}')


async def output_move(ctx, person):
    f = open(f'Chess_Bot/data/output-{person}.txt')
    out = f.readlines()
    f.close()

    game = data.data_manager.get_game(person)

    embed = discord.Embed(
        title=f'{ctx.author}\'s game', description=f'{whiteblack[game.color].capitalize()} to move.', color=0x5ef29c)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            embed.add_field(name='Computer moved', value=out[i][16:])
            break

    file = None

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('|'):
            get_image(person, i)

            file = discord.File(
                f'Chess_Bot/data/image-{person}.png', filename='board.png')
            embed.set_image(url=f'attachment://board.png')

            break

    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('GAME: '):
            game_str = out[i][6:-1].split(' ')
            game.moves.clear()

            for i in game_str:
                try:
                    game.moves.append(int(i))
                except:
                    pass

            break

    code = out[-3].strip()

    if code == 'DRAW':
        embed.description = 'Draw'
    elif (code == 'COMPUTER RESIGNED' and game.color == 1) or code == 'WHITE WON':
        embed.description = 'White won.'
    elif (code == 'COMPUTER RESIGNED' and game.color == 0) or code == 'BLACK WON':
        embed.description = 'Black won.'
    elif code == 'ILLEGAL MOVE PLAYED':
        embed.description = f'{whiteblack[game.color].capitalize()} to move.\nIllegal move played.'

    await ctx.message.reply(file=file, embed=embed)

    return code, game


async def log(person, client, ctx):
    log_channel = client.get_channel(798277701210341459)

    await log_channel.send(f'''Output for {ctx.author} (id = {ctx.author.id})
Request: {ctx.message.content}''', files=[
        discord.File(f'Chess_Bot/data/output-{person}.txt'),
        discord.File(f'Chess_Bot/data/input-{person}.txt'),
        discord.File(f'Chess_Bot/data/image-{person}.png')])
