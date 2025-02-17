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