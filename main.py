import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Credenciais do Spotify Developer carregadas das variáveis de ambiente
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state user-read-currently-playing user-top-read playlist-read-private user-library-read"
))

def get_minutes_seconds(sec):
    minutes = sec // 60
    seconds = sec % 60
    return minutes, seconds

# Printa o status atual no terminal
def get_current_status():
    curr_song = sp.current_playback()
    if curr_song:
        song_name = curr_song["item"]["name"]
        artists = ", ".join([artist["name"] for artist in curr_song["item"]["artists"]])
        progress = curr_song["progress_ms"] // 1000
        progress_minutes, progress_seconds = get_minutes_seconds(progress)
        duration = curr_song["item"]["duration_ms"] // 1000
        duration_minutes, duration_seconds = get_minutes_seconds(duration)
        if curr_song["is_playing"]:
            print(f"Tocando agora: {song_name} - {artists}")
        else:
            print(f"Pausado: {song_name} - {artists}")
        print(f"{progress_minutes:02d}:{progress_seconds:02d} / {duration_minutes:02d}:{duration_seconds:02d}")
    else:
        print("Nenhuma música tocando no momento.")
    
def get_top_songs(top_limit=10):
    # Coleta o TOP baseado nos últimos 6 meses (medium_term)
    results = sp.current_user_top_tracks(limit=top_limit, time_range="medium_term") 
    print(f"== Top {top_limit} músicas ==")
    for ind, song in enumerate(results["items"]):
        # Corrigido o f-string para exibir o nome da música e do álbum corretamente
        print(f'{ind + 1}) {song["name"]} ({song["album"]["name"]}) - {", ".join([artist["name"] for artist in song["artists"]])}')
    print()

# Printa o top artistas mais ouvidos
def get_top_artists(top_limit=10):
    # Coleta o TOP baseado nos últimos 6 meses (medium_term)
    results = sp.current_user_top_artists(limit=top_limit, time_range="medium_term")
    print(f"== Top {top_limit} artistas ==")
    for ind, artist in enumerate(results["items"]):
        print(f'{ind + 1}) {artist["name"]}')
    print()

# Printa os top artistas e músicas
get_top_artists()
get_top_songs()

# Printa o status atual a cada 2 segundos
while True:
    try:
        get_current_status()
        time.sleep(2)
    except Exception as e:
        # Às vezes gera um erro na troca de músicas, por isso deve ser tratado
        print(f"ERRO: {e}")
        time.sleep(2)
        