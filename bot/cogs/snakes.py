# coding=utf-8
import logging, aiohttp, random, wikipedia
from time import sleep
from bs4 import BeautifulSoup
from typing import Any, Dict
from discord.ext.commands import AutoShardedBot, Context, command
import asyncio

log = logging.getLogger(__name__)


class Snakes:
    """
    Snake-related commands
    """
    python_info = '''
                    Python (Programming Language)
                    \n
                    Python is powerful... and fast;\n
                    plays well with others;\n
                    runs everywhere;\n
                    is friendly & easy to learn;\n
                    is Open.
                    -------------------------------
                    Created by: Guido Van Rossum \n
                    Founded: 20th of February, 1991 \n
                    Official website: https://python.org
                '''

    def __init__(self, bot: AutoShardedBot):
        self.inputs = []
        self.bot = bot
        self.site = 'https://en.wikipedia.org/wiki/List_of_snakes_by_common_name'

    async def get_snek(self, embed, name: str = None) -> Dict[str, Any]:
        """
        Go online and fetch information about a snake

        The information includes the name of the snake, a picture of the snake, and various other pieces of info.
        What information you get for the snake is up to you. Be creative!

        If "python" is given as the snake name, you should return information about the programming language, but with
        all the information you'd provide for a real snake. Try to have some fun with this!

        :param name: Optional, the name of the snake to get information for - omit for a random snake
        :return: A dict containing information on a snake
        """
        name = str(name)
        site = self.site + name
        async with aiohttp.ClientSession() as session:
            async with session.get(site) as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, 'lxml')
                table = discord.Embed(title=soup.find('tbody'))

        if name.lower() == 'python':
            name = self.python_info
        else:
            embed = table

    @command()
    async def get(self, embed, ctx: Context, name: str = None,):
        """
        Go online and fetch information about a snake

        This should make use of your `get_snek` method, using it to get information about a snake. This information
        should be sent back to Discord in an embed.

        :param ctx: Context object passed from discord.py
        :param name: Optional, the name of the snake to get information for - omit for a random snake
        """
        # await ctx.send(BeautifulSoup(text, 'lxml').find("title"))
        if name:
            await ctx.send(await self.get_snek(name))
        else:
            ctx.send(embed=embed)
        # await ctx.send(name)

        # Any additional commands can be placed here. Be creative, but keep it to a reasonable amount!
    @command()
    async def snake(self, ctx: Context, x=50, y=30):
        board = """"""
        running = True
        head = [x//2, y//2]

        userID = ctx.author.id
        facing = 0

        board += "```\n " + "#" * x + "##"
        for yAxis in range(y):
            board += "\n #"
            for xAxis in range(x):
                if head == [xAxis, yAxis]:
                    board += "X"
                else:
                        board += "0"

            board += "#"
        board += "\n " + "#" * x + "##```"

        snakeBoard = await ctx.send(board)

        while running:
            for mess in self.inputs:
                if mess.author.id == userID:
                    await ctx.send("success")
                    self.inputs = []
                    if mess.content == "a":
                        facing = (facing - 1) % 4
                    if mess.content == "d":
                        facing = (facing + 1) % 4
                    break

            if facing == 0:
                head[1] -= 1
            elif facing == 1:
                head[0] += 1
            elif facing == 2:
                head[1] += 1
            else:
                head[0] -= 1

            board = """"""
            board += "```\n " + "#" * x + "##"
            for yAxis in range(y):
                board += "\n #"
                for xAxis in range(x):
                    if head == [xAxis, yAxis]:
                        board += "X"
                    else:
                        board += "0"

                board += "#"
            board += "\n " + "#" * x + "##```"

            await snakeBoard.edit(content=board)
            await asyncio.sleep(1)

    async def on_message(self, message):
        if message.content in ("w", "a", "s", "d"):
            self.inputs.append(message)
            await message.delete()


def setup(bot):
    bot.add_cog(Snakes(bot))
    log.info("Cog loaded: Snakes")
