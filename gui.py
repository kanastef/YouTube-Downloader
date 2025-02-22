import requests
from PIL import Image, ImageTk
from io import BytesIO
from download import search, download_video
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
class YTDownloaderGUI:
    def __init__(self, root):
        self.streams = None
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        tk.Label(root, text="Enter YouTube video URL: ", font=("Arial", 12)).pack(pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Search", command=self.fetch_video_data)
        self.search_button.pack(pady=5)

        self.video_title_label = tk.Label(root, text="Title: ", font=("Arial", 12))
        self.video_title_label.pack(pady=5)

        self.thumbnail_label = tk.Label(root)
        self.thumbnail_label.pack(pady=5)

        tk.Label(root, text="Select a format: ", font=("Arial", 12)).pack(pady=5)
        self.streams_combobox = ttk.Combobox(root, state="readonly", width=50)
        self.streams_combobox.pack(pady=5)

        self.download_button = tk.Button(root, text="Download", command=self.start_download, state="disabled")
        self.download_button.pack(pady=10)

        self.folder_path = tk.StringVar()
        self.browse_button = tk.Button(root, text="Select a folder for the download: ", command=self.select_folder)
        self.browse_button.pack(pady=5)

        self.folder_label = tk.Label(root, textvariable=self.folder_path, font=("Arial", 12))
        self.folder_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

    def fetch_video_data(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        video_data = search(url)
        if not video_data:
            messagebox.showerror("Error", "Failed to retrieve video information.")
            return

        self.video_title_label.config(text=f"Title: {video_data['title']}")
        response = requests.get(video_data["thumbnail_url"])
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((200,120), Image.LANCZOS)
        img = ImageTk.PhotoImage(img_data)
        self.thumbnail_label.config(image=img)
        self.thumbnail_label.image = img

        self.streams = video_data["streams"]
        stream_options = [
            f"{s.mime_type} - {s.resolution or s.abr} ({'Combined' if s.includes_audio_track else 'Video' if s.type == 'video' else 'Audio'})"
            for s in self.streams
        ]
        self.streams_combobox["values"] = stream_options
        self.streams_combobox.current(0)
        self.download_button.config(state="normal")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_download(self):
        selected_index = self.streams_combobox.current()
        if selected_index == -1:
            messagebox.showerror("Error", "Please select a format to download.")
            return

        itag = self.streams[selected_index].itag
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        self.download_button.config(state="disabled")
        self.progress_bar["value"] = 10
        self.root.update_idletasks()
        try:
            download_video(self.url_entry.get(), itag, folder)
            self.progress_bar["value"] = 100
            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")
        finally:
            self.download_button.config(state="normal")
            self.progress_bar["value"] = 0
