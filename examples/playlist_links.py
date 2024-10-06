from pytubefix import Playlist, YouTube
from pytubefix.exceptions import VideoUnavailable

playlist_url = 'https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab'

p = Playlist(playlist_url)

links = []

for url in p.video_urls:
	try:
		yt = YouTube(url)
	except VideoUnavailable:
		print(f'Video {url} is unavaialable, skipping.')
	else:
		print(f'Video URL: {url}')
		links.append(url)

# Вывод списка видео URL
print("\nAll available video URLs in the playlist:")
for link in links:
	print(link)
