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

# Configuration
config = {
    'CLIENT_ID': '439097970391121930',
    'INTERVAL': 5,
    'RECONNECT_DELAY': 10,
}


async def run_discordrpc(app):
    async with AsyncDiscordRpc.for_platform(config.get('CLIENT_ID')) as discord:
        await DiscordRpcService(discord, app, config).run()


def enable(app):
    asyncio.ensure_future(run_discordrpc(app))
    logger.debug('FeelUOwn Discord Plugin Enabled.')


def disable(app):
    logger.debug("FeelUOwn Discord Plugin Disabled.")
