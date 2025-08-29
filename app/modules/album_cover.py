import requests

def get_album_cover(artist: str | None, album: str | None) -> str | None:
    if not artist:
        return None
    if not album:
        return None

    query = f"{artist} {album}".replace(" ", "+")
    response = requests.get(f"https://itunes.apple.com/search?term={query}&entity=album").json()

    if not (response["resultCount"] > 0):
        return None

    results: dict = response.get("results")[0]
    album_cover: str = results.get("artworkUrl100", "")
    return album_cover.replace("100x100", "600x600")
