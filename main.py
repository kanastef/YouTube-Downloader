from download import *


def main():
    print("Welcome to YTDownloader!")
    url = input("Enter the YouTube Video URL: ")
    try:
        video_data = search(url)
        print(f"\nTitle: {video_data['title']}")
        print(f"Thumbnail: {video_data['thumbnail_url']}")

        print("Available formats: ")
        for stream in video_data["streams"]:
            print(f"{stream.itag}: {stream.mime_type} - {stream.resolution or 'Audio'}")
        itag = input("\nEnter the itag of the stream you want to download: ")
        download_folder = input("\nEnter the folder path for the download: ")
        download_video(url, int(itag), download_folder)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()