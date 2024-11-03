from typing import Callable, List
import discord

class DiscordChannel:
    def __init__(self):
        self.listeners: List[Callable[[discord.Message], None]] = []

    def subscribe(self, listener: Callable[[discord.Message], None]):
        self.listeners.append(listener)

    async def emit(self, msg: discord.Message):
        for listener in self.listeners:
            await listener(msg)

discord_chan = DiscordChannel()