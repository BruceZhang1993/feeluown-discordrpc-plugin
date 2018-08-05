# *-- coding: utf-8 --*
import logging
import asyncio
import time

from feeluown.app import CliApp
from fuocore.player import MpvPlayer as Player, State
from fuocore.models import SongModel
from PyQt5.QtCore import QObject
from feeluown_discordrpc.rpc import DiscordIpcClient, DiscordIpcError

logger = logging.getLogger(__name__)

CLIENT_ID = '439097970391121930'


class Discord(QObject):

    activity: dict = {}
    last_position = 0
    _rpc = None

    def __init__(self, app):
        if app.mode & app.GuiMode:
            super().__init__(parent=app)
        else:
            super().__init__(parent=None)
        self._app = app
        self._player: Player = self._app.player

    async def _ensure_connect(self):
        while not self._rpc:
            await asyncio.sleep(30)
            try:
                self._connect()
                self.handle_forever()
            except Exception as e:
                pass

    def _connect(self):
        try:
            logger.debug('Discord Connecting...')
            self._rpc = DiscordIpcClient.for_platform(CLIENT_ID)
        except Exception as e:
            raise e

    def subscribe(self):
        try:
            self._connect()
            logger.info('Discord Connected.')
            self.handle_forever()
        except Exception as e:
            logger.warning('Discord Connection Failed: %s' % e)
            asyncio.ensure_future(self._ensure_connect())

    def handle_forever(self):
        self._player.state_changed.connect(self.set_activity)
        self._player.media_changed.connect(self.set_activity)
        self._player.position_changed.connect(self.position_handler)

    def position_handler(self, position):
        position = self._player.position
        if position < self.last_position:
            self.last_position = position
            self.set_activity()
        elif position - self.last_position >= 5:
            self.last_position = position
            self.set_activity()

    def set_activity(self, arg1=None):
        activity = {}
        # Get current song
        current_song: SongModel = self._player.current_song
        if current_song:
            title = current_song.title
            artists = current_song.artists_name
            activity['details'] = "%s - %s" % (title, artists)
        else:
            activity['details'] = '空闲中'
        # Get player state and duration
        current_state: State = self._player.state
        if self._player.position:
            position = self.format_time(self._player.position)
        else:
            position = '00:00'
        if self._player.duration:
            duration = self.format_time(self._player.duration)
        else:
            duration = '00:00'
        if current_state == State.playing:
            state_name = '正在播放'
            activity['state'] = "%s [%s/%s]" % (state_name, position, duration)
        elif current_state == State.paused:
            state_name = '暂停播放'
            activity['state'] = "%s [%s/%s]" % (state_name, position, duration)
        elif current_state == State.stopped:
            state_name = '停止播放'
            activity['state'] = state_name
        else:
            state_name = '--'
            activity['state'] = '--'
        # Get timestamp
        if self._player.duration is not None:
            remaining = self._player.duration - self._player.position
            endtime = time.time() + remaining
            activity['timestamps'] = {
                'start': time.time() - self._player.position,
                'end': endtime
            }
        else:
            activity['timestamps'] = {
                'start': time.time() - self._player.position
            }
        # Set FeelUOwn image
        activity['assets'] = {'large_text': 'FeelUOwn',
                              'large_image': 'feeluown',
                              'small_text': state_name}

        if activity != self.activity:
            logger.debug('Syncing discord status.')
            try:
                self._rpc.set_activity(activity)
            except Exception as e:
                logger.debug(e)
                self._rpc._connect()
                self._rpc._do_handshake()
                self._rpc.set_activity(activity)
            self.activity = activity

    def unsubscribe(self):
        self._rpc.close()

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
