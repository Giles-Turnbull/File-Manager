import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the paths for the Downloads, Pictures, and Documents folders
downloads_folder = os.path.expanduser("~/Downloads")
pictures_folder = os.path.expanduser("~/Pictures")
documents_folder = os.path.expanduser("~/Documents")

# Create directories if they don't exist
os.makedirs(pictures_folder, exist_ok=True)
os.makedirs(documents_folder, exist_ok=True)

# Dictionary mapping file extensions to target folders
file_extensions = {
    "jpg": pictures_folder,
    "jpeg": pictures_folder,
    "png": pictures_folder,
    "gif": pictures_folder,
    "pdf": documents_folder,
    "pptx": documents_folder,
    "docx": documents_folder,
    "xlsx": documents_folder,
}

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        src_path = event.src_path
        file_extension = src_path.split('.')[-1].lower()

        if file_extension in file_extensions:
            target_folder = file_extensions[file_extension]
            dest_path = os.path.join(target_folder, os.path.basename(src_path))

            # Add a short delay (1 second) to allow the file to stabilize
            time.sleep(1)

            # Check if the file exists before moving it
            if os.path.exists(src_path):
                try:
                    # Move the file to the appropriate folder
                    shutil.move(src_path, dest_path)
                    print(f"Moved '{src_path}' to '{dest_path}'")
                except Exception as e:
                    print(f"Error moving '{src_path}': {str(e)}")
            else:
                print(f"File '{src_path}' does not exist.")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    try:
        print(f"Watching '{downloads_folder}' for new files...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
