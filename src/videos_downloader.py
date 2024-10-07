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
import shutil
from pytubefix import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

from titles_normalizer import normalize


def extract_number(s):
	# Извлекаем первое числовое значение из строки
	match = re.search(r'\d+', s)
	return int(match.group())


def get_best_video_stream(yt, max_resolution=1080):
	# max_resolution здесь это локальная переменная и учитывается аргумент, а не переменная глобального контекста
	print("(downloader) ---get_best_video_stream function---")
	streams = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc()
	for stream in streams:
		if stream.resolution == None:
			raise Exception("(downloader) stream.resolution is None")
		print("(downloader) ", stream.resolution, stream)
		# Получаем разрешение потока в виде числа
		if extract_number(stream.resolution) <= max_resolution:
			return stream
	return None


def move_file_to_directory(file_path, output_directory):
    """
    Функция для перемещения файла в указанную директорию.
    Если файл уже находится в правильной директории, ничего не делает.
    """

    # Получаем имя файла из пути
    file_name = os.path.basename(file_path)

    # Формируем новый путь для файла в указанной директории
    new_path = os.path.join(output_directory, file_name)

    # Проверяем, что файл существует и не находится уже в output_directory
    if os.path.exists(file_path) and file_path != new_path:

        # Создаем директорию, если она не существует
        os.makedirs(output_directory, exist_ok=True)

        # Перемещаем файл
        shutil.move(file_path, new_path)

        print(f"Captions moved {file_name} to {output_directory}")

    else:
        print(f"Captions {file_name} is already in the correct directory or does not exist.")


# Download subtitles if available
def download_subtitles(yt, output_directory='./', serial_number=-1):
	if yt.captions:
		# print(yt.captions)
		en_caption = yt.captions.get_by_language_code('en')  # You can change 'en' to any other language code if needed
		ru_caption = yt.captions.get_by_language_code('ru')  # You can change 'en' to any other language code if needed

		full_title = normalize(yt.title) if serial_number == -1 else str(serial_number)+"_"+normalize(yt.title)

		if en_caption:
			subtitle_file_path = en_caption.download(title=full_title, srt=True)
			# print(subtitle_file_path)
			if(subtitle_file_path):
				move_file_to_directory(subtitle_file_path, output_directory)

		if ru_caption:
			subtitle_file_path = ru_caption.download(title=full_title, srt=True)
			# print(subtitle_file_path)
			if(subtitle_file_path):
				move_file_to_directory(subtitle_file_path, output_directory)

	return None


def dowload_video(link, max_resolution, output_directory='./', serial_number=-1):
	yt = None

	# Handle exception
	try:
		# Object creation using YouTube
		# which was imported in the beginning
		yt = YouTube(link)

		print(f"(downloader) {yt.title}")

		print("(downloader) All possible streams:")
		for stream in yt.streams:
			print("(downloader) ", stream)

	except:
		raise Exception("(downloader) Connection Error")

	subtitle_file = download_subtitles(yt, output_directory, serial_number)

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

	print("(downloader) Selected:")
	print("(downloader) video_stream", video_stream)
	print("(downloader) audio_stream", audio_stream)

	video_file=""
	audio_file=""

	try:
		# Скачиваем видео
		video_file = video_stream.download(output_path=output_directory, filename='video.mp4')
		print('(downloader) Video downloaded successfully!')
	except: # pytube.exceptions.VideoUnavailable
		raise Exception("(downloader) Some Video Downloading Error!")

	try:	
		# Скачиваем аудио
		audio_file = audio_stream.download(output_path=output_directory, filename='audio.mp4')
		print('(downloader) Audio downloaded successfully!')
	except:
		raise Exception("(downloader) Some Audio Downloading Error!")

	# Объединяем видео и аудио
	video_clip = VideoFileClip(video_file)
	audio_clip = AudioFileClip(audio_file)

	final_clip = video_clip.set_audio(audio_clip)


	# libx264 - видеокодек H.264
	# aac - аудиокодек Advanced Audio
	full_title = normalize(yt.title) if serial_number == -1 else str(serial_number)+"_"+normalize(yt.title)
	final_clip.write_videofile(os.path.join(output_directory, full_title + ".mp4"), codec='libx264', audio_codec='aac')

	# Очистка временных файлов
	os.remove(video_file)
	os.remove(audio_file)


"""Пользовательские параметры

links - Links of the videos to be downloaded

Верхний предел качества скачиваемого, без него будет скачивать наилучшее доступное качество
max_resolution=1080 # 360, 480, 720, 1440 etc. or None
"""
def download_videos(videos, max_resolution=1080, output_directory="./"):
	try:
		for video in videos:
			if 'serial_number' in video:
				dowload_video(video['link'], max_resolution, output_directory, serial_number=video['serial_number'])
			else:
				dowload_video(video['link'], max_resolution, output_directory)

		print('(downloader) Task Completed!')

	except Exception as e:
		print('(downloader) Error: ', e)




if __name__ == "__main__":
	links=[
		"https://www.youtube.com/watch?v=rHLEWRxRGiM"
	]

	videos=[{'link':link} for link in links]
	download_videos(videos)
