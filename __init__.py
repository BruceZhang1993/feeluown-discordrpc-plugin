#!/usr/bin/env python3
# *-- coding: utf-8 --
import asyncio
import logging
from .discordrpc import DiscordRpcService
from .service.async import AsyncDiscordRpc

__alias__ = 'Discord RPC'
__version__ = '0.0.1'
__desc__ = "A plugin to enable discord rich presence."
logger = logging.getLogger('feeluown')
CLIENT_ID = '439097970391121930'


async def run_discordrpc(app):
    async with AsyncDiscordRpc.for_platform(CLIENT_ID) as discord:
        await DiscordRpcService(discord, app).run()


def enable(app):
    asyncio.ensure_future(run_discordrpc(app))
    logger.debug('Implemented enable')


def disable(app):
    pass
    logger.debug('Implemented disable')
