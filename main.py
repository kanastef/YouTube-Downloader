from download import *


def main():
    print("Welcome to YTDownloader!")
    while True:
        url = input("Enter the YouTube Video URL (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        try:
            video_data = search(url)
            print(f"\nTitle: {video_data['title']}")
            print(f"Thumbnail: {video_data['thumbnail_url']}")

            print("\nAvailable video and audio streams:")
            combined_streams = [stream for stream in video_data["streams"] if
                                stream.type == 'video' and stream.includes_audio_track]
            for index, stream in enumerate(combined_streams, start=1):
                print(f"{index}. Combined - Resolution: {stream.resolution}, Format: {stream.subtype.upper()}, itag: {stream.itag}")

            print("\nAvailable video streams:")
            video_streams = [stream for stream in video_data["streams"] if
                             stream.type == 'video' and not stream.includes_audio_track]
            for index, stream in enumerate(video_streams, start=1):
                print(f"{index}. Video - Resolution: {stream.resolution}, Format: {stream.subtype.upper()}, itag: {stream.itag}")

            print("\nAvailable audio streams:")
            audio_streams = [stream for stream in video_data["streams"] if
                             stream.type == 'audio' and not stream.includes_video_track]
            for index, stream in enumerate(audio_streams, start=1):
                print(f"{index}. Audio - Bitrate: {stream.abr}, Format: {stream.subtype.upper()}, itag: {stream.itag}")

            itag = input("\nEnter the itag of the stream you want to download (or type 'exit' to quit): ")
            if itag.lower() == 'exit':
                print("Exiting the program. Goodbye!")
                break
            download_folder = input("\nEnter the folder path for the download: ")
            download_video(url, int(itag), download_folder)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()