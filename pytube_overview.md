[[Software Library]]

Download a [[Youtube Video]] using [[Python]].

[GitHub](https://github.com/pytube/pytube)
[Documentation](https://pytube.io/)

---

Old Documentation:
https://pypi.org/project/pytube/7.0.16/

Раньше библиотека использовала зависимости и лицензировалась под MIT с copyright-ом. Сейчас библиотека dependency-free и распространяется под Unlicense, не признавая существование copyright-а.

Скачивает progressive видео, первое из всех стримов
```python
from pytube import YouTube
yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
.streams
.first()
.download()
```

```python
yt.streams
.all()
--->
<Stream: 
	itag="22"
	mime_type="video/mp4"
	res="720p" 
	fps="30fps"
	vcodec="avc1.64001F"
	acodec="mp4a.40.2"
>
```

- **Legacy/Progressive** - Stream-ы содержат оба аудио и видео
  Legacy стримы доступны до качества 720p.
- **Adaptive** - Stream-ы содержат либо только видео, либо только аудио
  Adaptive связаны с поддержкой [[Dynamic Adaptive Streaming over HTTP (MPEG-DASH)]]. Объединить отдельные медиа можно с [[FFmpeg]]


Отфильтровать стримы можно так:
```python
yt.streams
.filter(subtype='mp4', progressive=True)
.order_by('resolution')
.desc()
.all()
```

pytube можно пользовать как [[Command Line Interface (CLI)]].



----
# Examples

Вывод всех возможных стримов
```python
# Обязательно везде импортируем библиотеку
from pytube import YouTube
# Указываем ссылку на видео
yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
for stream in yt.streams:
    print(stream)
```

Как скачать видео лучшего качества
```python
from pytube import YouTube

yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')

# Фильтруем legacy/progressive mp4 
# и сортируем по убыванию качества
list_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().all()

# Вывод отфильтрованных стримов
for stream in list_streams:
    print(stream)

# Скачиываем видео лучшего качества
# и выводим пути к скаченному видео
print(list_streams[0].download())
```


Пример скачивания нескольких видео [geeksforgeeks](https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/)
```python
from pytube import YouTube

# Where to save
SAVE_PATH = "E:/"  # to_do

# Links of the videos to be downloaded
links = ["https://www.youtube.com/watch?v=xWOoBJUqlbI",
         "https://www.youtube.com/watch?v=xWOoBJUqlbI"]

for link in links:
    try:
        # Object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(link)
    except:
        # Handle exception
        print("Connection Error")

    # Get all streams and filter for mp4 files
    mp4_streams = yt.streams.filter(file_extension='mp4').all()

    # Get the video with the highest resolution
    d_video = mp4_streams[-1]

    try:
        # Download the video
        d_video.download(output_path=SAVE_PATH)
        print('Video downloaded successfully!')
    except:
        print("Some Error!")

print('Task Completed!')
```


Моя версия для скачивания Legacy/Progressive видео:
```python
from pytube import YouTube

# Links of the videos to be downloaded
links = ["http://youtube.com/watch?v=9bZkp7q19f0",
         "https://youtube.com/watch?v=wmiSb10F818"]

for link in links:
    try:
        # Object creation using YouTube
        # which was imported in the beginning
        yt = YouTube(link)
    except:
        # Handle exception
        print("Connection Error")

    # Get all streams and filter for mp4 files
    # Выполняется синхронно - не идет дальше, пока не выполнится
    mp4_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

    try:
        # Download the video
	    # Выполняется синхронно - не идет дальше, пока не выполнится
        print('Video downloaded successfully!', mp4_streams[0].download())
    except:
        print("Some Error!")

print('Task Completed!')
```


Legacy/Progressive скачивание ICT Course-а вроде все скачал без ошибок,
хотя https://ssyoutube.one выдавал ошибки на некоторых видео, я потом скачивал такие видео через https://y2meta.app
```python
links = [
"https://www.youtube.com/watch?v=lbvMfVsITsM",
"https://www.youtube.com/watch?v=jNKEEnzUcRw",
"https://www.youtube.com/watch?v=dq69gdvHvvw",
"https://www.youtube.com/watch?v=qh_LLCmqLXA",
"https://www.youtube.com/watch?v=Bb6Xcy37Ai0",
"https://www.youtube.com/watch?v=CJyrJ_no3BM",
"https://www.youtube.com/watch?v=6vPuWuahYXo",
"https://www.youtube.com/watch?v=MeBuwW9xJVc",
"https://www.youtube.com/watch?v=XqEbIOCmY5w",
"https://www.youtube.com/watch?v=7e9_BmQlVPc",
"https://www.youtube.com/watch?v=urWQqcHUqUw",
"https://www.youtube.com/watch?v=05I413k6b8o",
"https://www.youtube.com/watch?v=2zireQZ9AN8",
"https://www.youtube.com/watch?v=jX3Kz4E8BW0",
"https://www.youtube.com/watch?v=qjFEDhSzl0g",
"https://www.youtube.com/watch?v=P_r_CPzt9CM",
"https://www.youtube.com/watch?v=XFi3lFnFlH4",
"https://www.youtube.com/watch?v=ZfnxIZX-jfE",
"https://www.youtube.com/watch?v=cOxYGbuCX_I",
"https://www.youtube.com/watch?v=Ixe1W9_8Nnw",
"https://www.youtube.com/watch?v=fRpQDwGYDl4",
"https://www.youtube.com/watch?v=qYP0zi2Xkc8",
"https://www.youtube.com/watch?v=TYiwrHigHbw",
"https://www.youtube.com/watch?v=vBlyLRMJ8BU",
"https://www.youtube.com/watch?v=ebmePlEuTo0",
"https://www.youtube.com/watch?v=WK2DG4Y4tsE",
"https://www.youtube.com/watch?v=YFFTWDx1zUg",
"https://www.youtube.com/watch?v=fGqGxGbvpyg",
"https://www.youtube.com/watch?v=CvM1F6QhkHQ",
"https://www.youtube.com/watch?v=rQ-KSe06Vmk",
"https://www.youtube.com/watch?v=MaTrnjUOylA",
"https://www.youtube.com/watch?v=aypKKifsFqI",
"https://www.youtube.com/watch?v=S1k9oq4D85w",
"https://www.youtube.com/watch?v=twe5VZJXnw0",
"https://www.youtube.com/watch?v=Xvm6qw5tiY0"
]
```


Просто скачивания video и audio наилучшего качества и объединения
```python
import os

from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

# Скачиваем видео и аудио в наилучшем качестве
yt = YouTube('https://www.youtube.com/watch?v=wmiSb10F818')

# Выбираем видео с наилучшим качеством
video_stream = yt.streams.filter(adaptive=True, only_video=True).order_by('resolution').desc().first()

# Выбираем аудио с наилучшим качеством
audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()

print("All possible streams:")
for stream in yt.streams:
    print(stream)

print("Selected:")
print("video_stream", video_stream)
print("audio_stream", audio_stream)

# Скачиваем видео и аудио
video_file = video_stream.download(filename='video.mp4')
audio_file = audio_stream.download(filename='audio.mp4')

# Объединяем видео и аудио
video_clip = VideoFileClip(video_file)
audio_clip = AudioFileClip(audio_file)

final_clip = video_clip.set_audio(audio_clip)
# libx264 - видеокодек H.264
# aac - аудиокодек Advanced Audio Coding
final_clip.write_videofile("final_video2.mp4", codec='libx264', audio_codec='aac')

# Очистка временных файлов
os.remove(video_file)
os.remove(audio_file)
```


https://pytube.io/en/latest/user/exceptions.html
Так можно получить лист видео из плейлиста:
```python
from pytube import Playlist, YouTube
from pytube.exceptions import VideoUnavailable

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
```