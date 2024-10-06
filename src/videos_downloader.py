"""Docstring

Скачиваем видео с верхним порогом и аудио в наилучшем качестве.

По умолчанию скачивается наилучшее качество видео, но можно установить верхний порог.
Сначала скачивается video и audio поотдельности с помощью pytube, 
после они объединяются с помощью moviepy.

Видео скачивается рядом с этим файлом, 
можно кастомизировать, если указать output_path в stream.download() - pytube specification

Parameters
----------
links ([str])
	ссылки на youtube видео
max_resolution (int)
	верхний предел качества скачиваемого 

Returns
-------
void
	saves files

"""

import os
import re
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

from titles_normalizer import normalize


def extract_number(s):
	# Извлекаем первое числовое значение из строки
	match = re.search(r'\d+', s)
	return int(match.group())


def get_best_video_stream(yt, max_resolution=1080):
	# max_resolution здесь это локальная переменная и учитывается аргумент, а не переменная глобального контекста
	print("---get_best_video_stream function---")
	streams = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc()
	for stream in streams:
		if stream.resolution == None:
			raise Exception("stream.resolution is None")
		print(stream.resolution, stream)
		# Получаем разрешение потока в виде числа
		if extract_number(stream.resolution) <= max_resolution:
			return stream
	return None


# Download subtitles if available
def download_subtitles(yt, output_directory='./'):
	if yt.captions:
		en_caption = yt.captions.get_by_language_code('en')  # You can change 'en' to any other language code if needed
		if en_caption:
			subtitle_file = os.path.join(output_directory, normalize(yt.title) + ".srt")
			en_caption.download(title=normalize(yt.title), srt=True)
			return subtitle_file
	return None


def dowload_video(link, max_resolution, output_directory='./'):
	yt = None

	# Handle exception
	try:
		# Object creation using YouTube
		# which was imported in the beginning
		yt = YouTube(link)

		print("All possible streams:")
		for stream in yt.streams:
			print(stream)

	except:
		raise Exception("Connection Error")

	# Код выполняется синхронно - не выполняется следующая строчка, пока не выполнится настоящая

	video_stream = None

	if max_resolution == None:
		# Выбираем видео с наилучшим качеством
		video_stream = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc().first()
	else:
		# Выбираем видео с наилучшим качеством, но не выше определенного
		video_stream = get_best_video_stream(yt, max_resolution=1080)

	# Выбираем аудио с наилучшим качеством
	audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()

	print("Selected:")
	print("video_stream", video_stream)
	print("audio_stream", audio_stream)

	video_file=""
	audio_file=""

	try:
		# Скачиваем видео
		video_file = video_stream.download(output_path=output_directory, filename='video.mp4')
		print('Video downloaded successfully!')
	except: # pytube.exceptions.VideoUnavailable
		raise Exception("Some Video Downloading Error!")

	try:	
		# Скачиваем аудио
		audio_file = audio_stream.download(output_path=output_directory, filename='audio.mp4')
		print('Audio downloaded successfully!')
	except:
		raise Exception("Some Audio Downloading Error!")

	# Объединяем видео и аудио
	video_clip = VideoFileClip(video_file)
	audio_clip = AudioFileClip(audio_file)

	final_clip = video_clip.set_audio(audio_clip)

	subtitle_file = download_subtitles(yt, output_directory)

	# libx264 - видеокодек H.264
	# aac - аудиокодек Advanced Audio Coding
	final_clip.write_videofile(os.path.join(output_directory, normalize(yt.title) + ".mp4"), codec='libx264', audio_codec='aac')

	# Очистка временных файлов
	os.remove(video_file)
	os.remove(audio_file)


"""Пользовательские параметры

links - Links of the videos to be downloaded

Верхний предел качества скачиваемого, без него будет скачивать наилучшее доступное качество
max_resolution=1080 # 360, 480, 720, 1440 etc. or None
"""
def download_videos(links=["https://www.youtube.com/watch?v=wmiSb10F818"], max_resolution=1080, output_directory="./"):
	try:
		for link in links:
			dowload_video(link, max_resolution, output_directory)

		print('Task Completed!')

	except Exception as e:
		print(e)


# if __name__ == "__main__":
	# download_videos()
