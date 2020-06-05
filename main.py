from urllib.parse import urlparse
from tkinter import *
from urllib.request import Request
from dotenv import load_dotenv
import bs4
import os
import re
import requests
import spotipy
import spotipy.util as util
import time
import urllib.request


def main():
    def google_search(song_name, song_artist):
        url = f'https://www.google.com/search?q=metrolyrics{song_name}{song_artist}'
        result = []
        res = requests.get(url)
        if res.status_code == 200:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            for link in soup.find_all('a'):
                k = link.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    if urlparse(rul).netloc == 'www.metrolyrics.com':
                        result.append(rul)
                    else:
                        continue
                except:
                    continue
            if result:
                response = result[0]
            else:
                response = 'No song lyrics'
        else:
            response = 'Error 404'

        return response

    def metrolyrics(url_of_song):
        print("Searching the Lyrics...")
        time.sleep(5)
        page = urllib.request.Request(url_of_song, headers={'User-Agent': 'Mozilla/5.0'})
        infile = urllib.request.urlopen(page).read()
        res = infile.decode('ISO-8859-1')
        soup = bs4.BeautifulSoup(res, 'html.parser')
        lyrics_of_song = ''
        for el in soup.findAll("p", {"class": "verse"}):
            lyrics_of_song = lyrics_of_song + el.get_text()

        if lyrics_of_song:
            return lyrics_of_song
        else:
            return ""

    def create_gui(lyrics):
        window = Tk()
        window.title("Spot the Lyrics")
        window.state("zoomed")

        window.columnconfigure(0, minsize=900, weight=1)
        window.rowconfigure(0, minsize=768, weight=1)
        txt = Text(window, width=900, height=768, bg='gray25', fg='white')
        txt.grid(column=0, row=0)

        txt.insert("1.0", lyrics)

        window.mainloop()

    load_dotenv()
    username = os.getenv('username')
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    redirect_uri = os.getenv('redirect_uri')

    token = util.prompt_for_user_token(username,
                                       "user-read-currently-playing",
                                       client_id,
                                       client_secret,
                                       redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playing_track()
        if results:
            song = results["item"]["name"]
            artist = results['item']['artists'][0]['name']
            link = google_search(song, artist)
            try:
                lyrics = metrolyrics(link)
                create_gui(lyrics)
            except:
                create_gui(link)
        else:
            create_gui('No song is playing right now!')
    else:
        create_gui("Can't get token for" + username)


if __name__ == '__main__':
    main()
