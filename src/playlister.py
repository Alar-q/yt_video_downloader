from pytubefix import Playlist, YouTube
from pytubefix.exceptions import VideoUnavailable


def playlist_links(playlist_url):

	p = Playlist(playlist_url)

	print(f'Playlist: {p.title}')

	# Пользовательские параметры
	# Links of the videos to be downloaded

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
	# print("\nAll available video URLs in the playlist:")
	# for link in links:
	# 	print(link)

	return p.title, links


# if __name__ == "__main__":
	# playlist_links("https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab")
