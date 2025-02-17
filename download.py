import os
import pytubefix
import re

def search(url):
    """
    Fetches video information and available streams from a given YouTube URL.

    This function retrieves metadata (title and thumbnail URL) and filters
    available streams to include only MP4 video and audio formats.

    :param url: The URL of the YouTube video

    :return: A dictionary containing the previously mentioned information about the video.

    """
    video = pytubefix.YouTube(url=url)
    streams = video.streams
    return {
        "streams":
            [stream for stream in streams
            if stream.mime_type == "video/mp4"
            or stream.mime_type == "audio/mp4"],
        "thumbnail_url": video.thumbnail_url,
        "title": video.title,
        "originalStream": streams
    }

def download_video(url, itag, download_folder):
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
