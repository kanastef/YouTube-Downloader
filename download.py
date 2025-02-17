import pytube

def search(url):
    """
    Fetches video information and available streams from a given YouTube URL.

    This function retrieves metadata (title and thumbnail URL) and filters
    available streams to include only MP4 video and audio formats.

    :param url: The URL of the YouTube video

    :return: A dictionary containing the previously mentioned information about the video.

    """
    video = pytube.YouTube(url=url)
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

def download_video(url, itag, output_path="downloads"):
    try:
        video = pytube.YouTube(url=url)
        stream = video.streams.get_by_itag(itag)

        if not stream:
            print("Invalid itag selected: ")
            return

        print("Downloading {video.title}...")
        stream.download(output_path)
        print("Download complete!")
    except Exception as e:
        print(f"Error: {e}")
