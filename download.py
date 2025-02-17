import os
import pytubefix
import re

def search(url):
    """
    Fetches video information and available streams from a given YouTube URL.

    This function retrieves the video title, thumbnail URL, and available streams.
    The streams are categorized into:
    - **Combined streams**: Contain both video and audio.
    - **Video-only streams**: Do not include audio.
    - **Audio-only streams**: Contain only the audio track.

    Streams are sorted in descending order:
    - Video streams are sorted by resolution (highest to lowest).
    - Audio streams are sorted by bitrate (highest to lowest).

    :param url: The URL of the YouTube video

    :return: A dictionary containing the previously mentioned information about the video.

    """
    try:
        video = pytubefix.YouTube(url=url)
        streams = video.streams
        video_streams = [s for s in streams if s.type == 'video' and not s.includes_audio_track]
        audio_streams = [s for s in streams if s.type == 'audio']
        combined_streams = [s for s in streams if s.type == 'video' and s.includes_audio_track]
        sorted_video_streams = sorted(video_streams, key=lambda s: (int(s.resolution.replace('p', '') if s.resolution else 0)), reverse=True)
        sorted_audio_streams = sorted(audio_streams, key=lambda s: (int(s.abr.replace('kbps', '') if s.abr else 0)),
                                      reverse=True)
        sorted_combined_streams = sorted(combined_streams,
                                         key=lambda s: (int(s.resolution.replace('p', '') if s.resolution else 0)),
                                         reverse=True)
        return {
            "streams":
                sorted_combined_streams + sorted_video_streams + sorted_audio_streams,
            "thumbnail_url": video.thumbnail_url,
            "title": video.title,
            "originalStream": streams
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def download_video(url, itag, download_folder):
    """
    Downloads a YouTube video or audio stream based on the selected itag.

    This function retrieves the specified stream by its itag, downloads it to the given folder,
    and saves it with a sanitized filename.

    If the specified folder does not exist, the function notifies the user and exits.
    If the download is successful, it confirms the saved file location. Otherwise, it displays an error message.

    :param url: The URL of the YouTube video.
    :param itag: The itag of the desired stream (used to identify a specific quality/format).
    :param download_folder: The path to the folder where the file will be saved.

    """
    if not os.path.isdir(download_folder):
        print("The folder path is invalid or doesn't exist. Please check the path and try again.")
        return
    try:
        video = pytubefix.YouTube(url=url)
        stream = video.streams.get_by_itag(itag)

        if not stream:
            print("Invalid itag selected: ")
            return

        print(f"Downloading {video.title}...")
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', video.title)
        file_path = os.path.join(download_folder, f"{sanitized_title}.{stream.subtype}")
        stream.download(output_path=download_folder, filename=f"{sanitized_title}.{stream.subtype}")
        if os.path.exists(file_path):
            print(f"Download complete. File saved to: {os.path.abspath(file_path)}")
        else:
            print("Download failed.")
    except Exception as e:
        print(f"Error: {e}")
