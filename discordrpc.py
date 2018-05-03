#!/usr/bin/env python3
# *-- coding: utf-8 --
import asyncio
import logging
import time
from typing import Dict, Optional

from PyQt5.QtCore import QThread
from fuocore.core.player import State
from quamash import QThreadExecutor

from .service.async import AsyncDiscordRpc, DiscordRpcError, JSON

logger = logging.getLogger('feeluown')


class DiscordRpcService:

    last_activity: Optional[JSON] = None

    def __init__(self, discord: AsyncDiscordRpc, app, config):
        super().__init__()
        self._app = app
        self.discord = discord
        self.config = config

        # TODO: Binding events
        # self._app.player.stateChanged.connect(self._tick_once)
        # self._app.player.signal_player_song_changed.connect(self._tick_once)

    def _tick_once(self, *args, **kwargs):
        asyncio.ensure_future(self.tick())

    async def try_reconnect(self):
        if not self.discord.connected:
            try:
                await self.discord.connect()
            except Exception as e:
                logger.error("%s: Reconnect error." % e)
        else:
            return

    async def connect_discord(self):
        if self.discord.connected:
            return
        while True:
            try:
                await self.discord.connect()
            except DiscordRpcError:
                logger.warning("Failed to connect to discord client")
                await asyncio.sleep(self.config.get('RECONNECT_DELAY'))
                continue
            except Exception as err:
                logger.warning("%s" % err)
                await asyncio.sleep(self.config.get('RECONNECT_DELAY'))
                continue
            else:
                break

    async def run(self):
        await self.connect_discord()

        while True:
            try:
                await self.tick()
            except Exception as err:
                logger.warning("%s: Reconnecting..." % err)
            finally:
                await self.try_reconnect()
            await asyncio.sleep(self.config.get('INTERVAL'))

    async def tick(self) -> None:
        player = self._app.player
        activity: JSON = {}
        current_song = player.current_song

        if current_song:
            title = current_song.title
            artists = current_song.artists_name
        else:
            title = '...'
            artists = '...'
        position = player.player.position
        duration = player.player.duration
        state = player.player.state

        if state == State.playing:
            state_name = '正在播放'
        elif state == State.paused:
            state_name = '暂停播放'
        else:
            state_name = '停止播放'

        if current_song:
            activity['details'] = "%s - %s" % (title, artists)
        else:
            activity['details'] = "空闲中"

        if state == State.stopped:
            activity['state'] = "%s" % state_name
        else:
            position_str = self.format_time(position)
            duration_str = self.format_time(duration)
            activity['state'] = "%s [%s/%s]" % (state_name, position_str, duration_str)

        if duration is not None:
            remaining = duration - position
            end_time = time.time() + remaining
            activity['timestamps'] = {
                'start': time.time() - position,
                'end': end_time
            }
        else:
            activity['timestamps'] = {
                'start': time.time() - position
            }

        activity['assets'] = {'large_text': 'FeelUOwn',
                              'large_image': 'feeluown',
                              'small_text': state_name}

        if activity != self.last_activity:
            logger.debug('Syncing discord status.')
            await self.discord.set_activity(activity)
            self.last_activity = activity

    @staticmethod
    def format_time(seconds):
        if seconds is None:
            return "00:00"
        seconds = int(seconds)
        if seconds > 60:
            minutes = int(seconds / 60)
            seconds = seconds - int(minutes * 60)
        else:
            minutes = 0
        return "%s:%s" % (str(minutes).zfill(2), str(seconds).zfill(2))
