# *-- coding: utf-8 --*
import logging

from .discord import Discord

__alias__ = 'Discord Rich Presence'
__version__ = '0.0.1'
__feeluown_version__ = '2.0.0'
__desc__ = 'Discord RPC Rich Presence Support.'

logger = logging.getLogger(__name__)
loader: Discord = None


def enable(app):
    global loader
    loader = Discord(app)
    loader.subscribe()
    logger.info(__alias__ + ' enabled.')


def disable(app):
    global loader
    loader.unsubscribe()
    logger.info(__alias__ + ' disabled.')
