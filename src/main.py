from pytubefix import Playlist, YouTube
from videos_downloader import download_videos
from titles_normalizer import normalize


def binary_confirm(prompt):
    """
    запрос подтверждения через консоль.
    """
    while True:
        answer = input(f"{prompt} (y/n): ").lower()
        if answer in ['y', 'n']:
            return answer == 'y'
        else:
            print("\nEnter ‘y’ for confirmation or ‘n’ for cancellation, please.")


def confirm(prompt):
   while True:
        answer = input(f"{prompt} (y/n/a/x): ").lower()
        if answer in ['y', 'n', 'a', 'x']:
            return answer
        else:
            print("\nPlease enter ‘y’ for yes, ‘n’ for no, ‘a’ to select all else, or ‘x’ to reject all else.")


def collect_videos_to_download(playlists):
    """
    Collects all confirmed to download videos from playlists.
    """
    confirmed = []

    for playlist_url in playlists:

        playlist = Playlist(playlist_url)

        video_urls = playlist.video_urls

        # Запрашиваем подтверждение для плейлиста
        if binary_confirm(f"\nPlaylist name is '{playlist.title}'. Do you want to process this playlist?"):
            confirmed_videos = []
            for i, link in enumerate(video_urls):
                yt = YouTube(link)

                # Запрашиваем подтверждение для каждого видео
                answer = confirm(f"\nDownload video named '{yt.title}'?")

                if answer == 'a':
                    # Выбираем нынешнее и все оставшиеся видео
                    for j, linkj in enumerate(video_urls):
                        if(j<i):
                            continue
                        ytj = YouTube(linkj)
                        confirmed_videos.append({'title': ytj.title, 'link': linkj, 'serial_number':j+1})

                    break

                elif answer == 'x':
                    print(f"\nSkipping all videos in playlist: '{playlist.title}'")
                    break

                elif answer == 'y':
                    confirmed_videos.append({'title': yt.title, 'link': link, 'serial_number':i+1})

            print("confirmed_videos:", confirmed_videos)

            # Если были выбраны видео для скачивания
            if len(confirmed_videos) > 0:
                confirmed.append((playlist.title, confirmed_videos))
            else:
                print(f"\nNo videos selected from playlist: '{playlist.title}'")

        else:
            print(f"\nSkipping playlist: '{playlist.title}'")

    return confirmed




if __name__ == "__main__":
    playlists = [
        'https://www.youtube.com/playlist?list=PL6-BrcpR2C5Q1ivGTQcglILJG6odT2oCY',
        'https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab',
        'https://www.youtube.com/playlist?list=PL6-BrcpR2C5RYoCAmC8VQp_rxSh0i_6C6'
    ]

    # Вначале собираем все подтверждения по видео
    confirmed = collect_videos_to_download(playlists)


    # Убеждаемся, что все правильно
    print('\n\n------\nFollowing selected videos from the playlists will be downloaded:\n')
    for title, videos in confirmed:
        print('------')
        print(title)
        for video in videos:
            print('     ', video['title'])
        print('------\n\n')


    # Если есть подтвержденные видео, начинаем скачивание
    if len(confirmed) > 0:
        print("\nStarting the download process...")
        for title, videos in confirmed:
            print(f"\nStarting download for playlist: '{title}' with {len(videos)} video(s).")
            download_videos(videos, max_resolution=1080, output_directory=f"./{normalize(title)}")

    else:
        print("\nNo videos selected for download.")

