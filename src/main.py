from pytubefix import YouTube
from playlister import playlist_links
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
            print("Enter ‘y’ for confirmation or ‘n’ for cancellation, please.")

def confirm(prompt):
   while True:
        answer = input(f"{prompt} (y/n/a/x): ").lower()
        if answer in ['y', 'n', 'a', 'x']:
            return answer
        else:
            print("Please enter ‘y’ for yes, ‘n’ for no, ‘a’ to select all, or ‘x’ to reject all.")


def collect_videos_to_download(playlists):
    """
    Collects all confirmed to download videos from playlists.
    """
    confirmed = []

    for playlist in playlists:
        title, links = playlist_links(playlist_url=playlist)

        # Запрашиваем подтверждение для плейлиста
        if binary_confirm(f"\nPlaylist name is '{title}'. Do you want to process this playlist?"):
            confirmed_videos = []
            for i, link in enumerate(links):
                yt = YouTube(link)

                # Запрашиваем подтверждение для каждого видео
                answer = confirm(f"\nDownload video named '{yt.title}'?")

                if answer == 'a':
                    # Выбираем все видео из плейлиста
                    for j, linkj in enumerate(links):
                        if(j<i):
                            continue
                        ytj = YouTube(linkj)
                        confirmed_videos.append({'title': ytj.title, 'link': linkj, 'serial_number':j})

                    break

                elif answer == 'x':
                    print(f"\nSkipping all videos in playlist: '{title}'")
                    break

                elif answer == 'y':
                    confirmed_videos.append({'title': yt.title, 'link': link, 'serial_number':i})

            print(confirmed_videos)

            # Если были выбраны видео для скачивания
            if confirmed_videos:
                confirmed.append((title, confirmed_videos))
            else:
                print(f"\nNo videos selected from playlist: '{title}'")
        else:
            print(f"\nSkipping playlist: '{title}'")

    return confirmed




if __name__ == "__main__":
    playlists = [
        'https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab',
        'https://www.youtube.com/playlist?list=PL6-BrcpR2C5RYoCAmC8VQp_rxSh0i_6C6'
    ]

    # Вначале собираем все подтверждения по видео
    confirmed = collect_videos_to_download(playlists)


    print('\n\n')
    for title, videos in confirmed:
        print('------')
        print(title)
        for video in videos:
            print('     ', video['title'])
        print('------\n\n')


    # Если есть подтвержденные видео, начинаем скачивание
    if confirmed:
        print("\nStarting the download process...")
        for title, videos in confirmed:
            print(f"\nStarting download for playlist: '{title}' with {len(videos)} video(s).")
            # links = [video['link'] for video in videos]
            # print("links", links)
            download_videos(videos, max_resolution=1080, output_directory=f"./{normalize(title)}")

    else:
        print("\nNo videos selected for download.")

