# custom classes replacing the ones in pypresence
# (the following classes still use some core components of pypresence though)
# to allow the status to say "Listening to" instead of "Playing"

import os
import json
import time
from pypresence.baseclient import BaseClient
from pypresence.utils import get_event_loop, remove_none
from typing import Any, Optional

class Payload:
    def __init__(self, data: dict[str, Any], clear_none: bool = True) -> None:
        if clear_none:
            data = remove_none(data)
        self.data = data

    def __str__(self) -> str:
        return json.dumps(self.data, indent=2)

    @staticmethod
    def time() -> float:
        return time.time()

    @classmethod
    def set_activity(cls, pid: int = os.getpid(),
                     state: Optional[str] = None, details: Optional[str] = None,
                     start: Optional[int] = None, end: Optional[int] = None,
                     large_image: Optional[str] = None, large_text: Optional[str] = None,
                     small_image: Optional[str] = None, small_text: Optional[str] = None,
                     party_id: Optional[str] = None, party_size: Optional[list[int]] = None,
                     join: Optional[str] = None, spectate: Optional[str] = None,
                     match: Optional[str] = None, buttons: Optional[list[dict[str, str]]] = None,
                     instance: bool = True, activity: Optional[bool] = True,
                     activity_type: int = 0, _rn: bool = True) -> 'Payload':

        # Convert timestamps to integers if provided
        if start is not None:
            start = int(start)
        if end is not None:
            end = int(end)

        if activity is None:
            act_details = None
            clear = True
        else:
            act_details = {
                "state": state,
                "details": details,
                "type": activity_type,
                "timestamps": {
                    "start": start,
                    "end": end
                },
                "assets": {
                    "large_image": large_image,
                    "large_text": large_text,
                    "small_image": small_image,
                    "small_text": small_text
                },
                "party": {
                    "id": party_id,
                    "size": party_size
                },
                "secrets": {
                    "join": join,
                    "spectate": spectate,
                    "match": match
                },
                "buttons": buttons,
                "instance": instance
            }
            clear = False

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": act_details
            },
            "nonce": f'{cls.time():.20f}'
        }
        
        if _rn:
            clear = _rn
        return cls(payload, clear)

    @classmethod
    def authorize(cls, client_id: str, scopes: list[str]) -> 'Payload':
        payload = {
            "cmd": "AUTHORIZE",
            "args": {
                "client_id": str(client_id),
                "scopes": scopes
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def authenticate(cls, token: str) -> 'Payload':
        payload = {
            "cmd": "AUTHENTICATE",
            "args": {
                "access_token": token
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_guilds(cls) -> 'Payload':
        payload = {
            "cmd": "GET_GUILDS",
            "args": {},
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_guild(cls, guild_id: str) -> 'Payload':
        payload = {
            "cmd": "GET_GUILD",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_channels(cls, guild_id: str) -> 'Payload':
        payload = {
            "cmd": "GET_CHANNELS",
            "args": {
                "guild_id": str(guild_id),
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_channel(cls, channel_id: str) -> 'Payload':
        payload = {
            "cmd": "GET_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def set_user_voice_settings(cls, user_id: str, pan_left: Optional[float] = None,
                                pan_right: Optional[float] = None, volume: Optional[int] = None,
                                mute: Optional[bool] = None) -> 'Payload':
        payload = {
            "cmd": "SET_USER_VOICE_SETTINGS",
            "args": {
                "user_id": str(user_id),
                "pan": {
                    "left": pan_left,
                    "right": pan_right
                },
                "volume": volume,
                "mute": mute
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload, True)

    @classmethod
    def select_voice_channel(cls, channel_id: str) -> 'Payload':
        payload = {
            "cmd": "SELECT_VOICE_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_selected_voice_channel(cls) -> 'Payload':
        payload = {
            "cmd": "GET_SELECTED_VOICE_CHANNEL",
            "args": {},
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def select_text_channel(cls, channel_id: str) -> 'Payload':
        payload = {
            "cmd": "SELECT_TEXT_CHANNEL",
            "args": {
                "channel_id": str(channel_id),
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def subscribe(cls, event: str, args: Optional[dict[str, Any]] = None) -> 'Payload':
        if args is None:
            args = {}
        payload = {
            "cmd": "SUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def unsubscribe(cls, event: str, args: Optional[dict[str, Any]] = None) -> 'Payload':
        if args is None:
            args = {}
        payload = {
            "cmd": "UNSUBSCRIBE",
            "args": args,
            "evt": event.upper(),
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def get_voice_settings(cls) -> 'Payload':
        payload = {
            "cmd": "GET_VOICE_SETTINGS",
            "args": {},
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def set_voice_settings(cls, _input: Optional[dict[str, Any]] = None, output: Optional[dict[str, Any]] = None,
                           mode: Optional[dict[str, Any]] = None, automatic_gain_control: Optional[bool] = None,
                           echo_cancellation: Optional[bool] = None, noise_suppression: Optional[bool] = None,
                           qos: Optional[bool] = None, silence_warning: Optional[bool] = None,
                           deaf: Optional[bool] = None, mute: Optional[bool] = None) -> 'Payload':
        payload = {
            "cmd": "SET_VOICE_SETTINGS",
            "args": {
                "input": _input,
                "output": output,
                "mode": mode,
                "automatic_gain_control": automatic_gain_control,
                "echo_cancellation": echo_cancellation,
                "noise_suppression": noise_suppression,
                "qos": qos,
                "silence_warning": silence_warning,
                "deaf": deaf,
                "mute": mute
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload, True)

    @classmethod
    def capture_shortcut(cls, action: str) -> 'Payload':
        payload = {
            "cmd": "CAPTURE_SHORTCUT",
            "args": {
                "action": action.upper()
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def send_activity_join_invite(cls, user_id: str) -> 'Payload':
        payload = {
            "cmd": "SEND_ACTIVITY_JOIN_INVITE",
            "args": {
                "user_id": str(user_id)
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)

    @classmethod
    def close_activity_request(cls, user_id: str) -> 'Payload':
        payload = {
            "cmd": "CLOSE_ACTIVITY_REQUEST",
            "args": {
                "user_id": str(user_id)
            },
            "nonce": f'{cls.time():.20f}'
        }
        return cls(payload)


class Presence(BaseClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def update(
        self, pid: int = os.getpid(),
        state: Optional[str] = None, details: Optional[str] = None,
        start: Optional[int] = None, end: Optional[int] = None,
        large_image: Optional[str] = None, large_text: Optional[str] = None,
        small_image: Optional[str] = None, small_text: Optional[str] = None,
        party_id: Optional[str] = None, party_size: Optional[list[int]] = None,
        join: Optional[str] = None, spectate: Optional[str] = None,
        match: Optional[str] = None, buttons: Optional[list[dict[str, str]]] = None,
        instance: bool = True, activity_type: int = 2, 
        payload_override: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        if payload_override is None:
            payload = Payload.set_activity(
                pid=pid, state=state, details=details, start=start, end=end,
                large_image=large_image, large_text=large_text,
                small_image=small_image, small_text=small_text, party_id=party_id,
                party_size=party_size, join=join, spectate=spectate,
                match=match, buttons=buttons, instance=instance, 
                activity=True, activity_type=activity_type
            )
        else:
            payload = Payload(payload_override)
        
        self.send_data(1, payload.data)
        return self.loop.run_until_complete(self.read_output())

    def clear(self, pid: int = os.getpid()) -> dict[str, Any]:
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload.data)
        return self.loop.run_until_complete(self.read_output())

    def connect(self) -> None:
        self.update_event_loop(get_event_loop())
        self.loop.run_until_complete(self.handshake())

    def close(self) -> None:
        if self.sock_writer is not None:
            self.send_data(2, {'v': 1, 'client_id': self.client_id})
            self.sock_writer.close()
        if hasattr(self, 'loop') and self.loop is not None:
            self.loop.close()
