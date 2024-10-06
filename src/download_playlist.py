from playlister import playlist_links
from videos_downloader import download_videos
from titles_normalizer import normalize

playlists = ['https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab']

for playlist in playlists:
    title, links = playlist_links(playlist_url=playlist)
    print(title, links)

    download_videos(links, max_resolution=1080, output_directory=f"./{normalize(title)}")

