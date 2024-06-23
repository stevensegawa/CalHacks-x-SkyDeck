import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

class PhotoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.process(event.src_path)

    def process(self, file_path):
        # Wait a bit to ensure the file is completely written
        time.sleep(2)
        if file_path.lower().endswith(('jpg', 'jpeg', 'heic')):
            try:
                print(f'Trying to open: {file_path}')
                with open(file_path, 'rb') as f:
                    image = Image.open(f)
                    image.verify()  # Verify that this is an image
                image = Image.open(file_path)  # Reopen since verify() must be followed by re-open
                # Save the image as 'converted_img.png' in the current directory
                current_directory = os.path.dirname(os.path.abspath(__file__))
                png_path = os.path.join(current_directory, 'images/converted_img.png')
                image.save(png_path, 'PNG')
                print(f'Converted {file_path} to {png_path}')
            except Exception as e:
                print(f'Failed to convert {file_path}: {e}')

if __name__ == "__main__":
    path_to_watch = r'C:/Users/steve/Dropbox'  # Replace with your actual path
    event_handler = PhotoHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    print(f'Starting to watch {path_to_watch} for new photos...')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
