import sys
import time
import json
from modules.rpc import Presence
from modules.album_cover import get_album_cover
from win32com.client import Dispatch
from datetime import datetime, timezone, timedelta
from urllib.parse import quote as encode_uri
from typing import Any

try:
    itunes_app_cd = Dispatch("iTunes.Application")
except:
    print("Dispatch connection method failed. Trying other ID...")
    try:
        itunes_app_cd = Dispatch("iTunes.Application.1")
    except:
        print(f"All iTunes connection methods failed. Is iTunes installed and running?")
        sys.exit(1)

def _getPlayerState() -> str | None:
    if not itunes_app_cd:
        return "Not Opened"

    match itunes_app_cd.PlayerState:
        case 0:
            return "Paused" if itunes_app_cd.currentTrack and itunes_app_cd.currentTrack.name else "Stopped"

        case 1:
            return "Playing"

def _getCurrentTrack() -> str:
    data: dict[str, Any] = {}

    try:
        currentTrack = itunes_app_cd.currentTrack
        data = {
            "name": currentTrack.name,
            "artist": currentTrack.artist,
            "album": currentTrack.album,
            "kind": currentTrack.kind,
            "duration": currentTrack.duration,
            "genre": currentTrack.genre,
            "year": currentTrack.year,
            "elapsed": itunes_app_cd.PlayerPosition,
            "state": _getPlayerState(),
        }

    except Exception:
        data = {
            "state": _getPlayerState(),
        }

    return json.dumps(data)

def play() -> None:
    itunes_app_cd.play()

class iTunesBridge:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}
        self.currentSong: dict[str, Any] = {}

        try:
            self.currentSong = json.loads(_getCurrentTrack())
        except Exception:
            self.currentSong = {
                "state": "Loading/Not playing"
            }

    def getCurrentSong(self) -> dict[str, Any]:
        self.currentSong = json.loads(_getCurrentTrack())
        return self.currentSong

    def getState(self) -> str:
        self.data["state"] = (_getPlayerState() or "").strip()
        self.currentSong["state"] = self.data["state"]
        return self.data["state"]

try:
    rpc = Presence('1411022045910929539')
    rpc.connect()
except Exception:
    print("Discord is not installed or is not running.")
    sys.exit(1)

itunes_app = iTunesBridge()

state: str = "Not Opened"
currentSong: dict[str, Any] = {}
startDate: datetime = datetime.now(tz=timezone.utc)

def update():
    now = datetime.now(tz=timezone.utc)
    state: str = ""
    currentSong: dict[str, Any] = itunes_app.getCurrentSong()
    song_name: str | None = currentSong.get("name", None)
    song_artist: str | None = currentSong.get("artist", None)
    song_album: str | None = currentSong.get("album", None)
    song_elapsed: str | None = currentSong.get("elapsed", None)

    if currentSong:
        state = itunes_app.getState()

    if song_name and " - " in song_name:
        split = song_name.split(" - ")
        song_artist = split[0] if len(split) > 1 else None
        song_name = split[1] if len(split) > 1 else song_name

    startDate = now - timedelta(seconds=int(song_elapsed or 0))
    ac: str | None = get_album_cover(song_artist, song_album)
    playing: bool = state == "Playing"

    print(f"Updating RPC... ({f'Song: {song_name} by {song_artist}' if playing else 'Nothing playing, clearing status'})")

    if playing:
        rpc.update(
            state=(song_artist or "Unknown Artist"),
            details=(song_name or "Unknown Song"),
            start=int(startDate.timestamp()),
            large_image=ac,
            large_text=(song_album or "Unknown Album"),
            activity_type=2  # listening
        )
    else:
        rpc.clear()


if __name__ == "__main__":
    try:
        while True:
            update()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
