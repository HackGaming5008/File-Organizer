
####################### IMPORTS ##################

import shutil
import pathlib
from pathlib import Path

################## VARIABLES ##################

# Path
path = Path.home() / "Downloads"

# Extensions
image_ext = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
zip_ext = [".zip", ".rar", ".7z", ".tar", ".gz"]
vid_ext = [".mp4", ".avi", ".mkv", ".mov", ".flv"]
music_ext = [".mp3", ".wav", ".flac", ".ogg"]
code_ext = [".py", ".cpp", ".c", ".js", ".html", ".css"]
pdf_ext = [".pdf"]
docx_ext = [".docx", ".doc", ".xlsx", ".pptx"]

#################### FUNCTIONS ###################


def move_files(src, dist, files):
    if files:
        for file in files:
            src_file = src / file
            dist_file = dist / file
            shutil.move(src_file, dist_file)
            print(f"Moved {file}")
    else:
        print(f"No files to move in {dist_file.name}")


def delete_empty_folder(folder):
    try:
        folder.rmdir()
        print(f"Deleted empty folder: {folder.name}")
    except OSError:
        print(f"Could not delete folder: {folder.name} (not empty)")


##################### MAIN ######################

class Orgonaizer():
    def __init__(self):
        super().__init__()

        self.results = []

        self.catagories = {
            "Images": [[], image_ext],
            "Zips": [[], zip_ext],
            "Videos": [[], vid_ext],
            "Music": [[], music_ext],
            "Code": [[], code_ext],
            "PDFs": [[], pdf_ext],
            "Docx": [[], docx_ext],
            "Documents": [[], []]
        }

        self.delete_empty_folders = False

    def scanFolder(self, folder_path):
        for entry in folder_path.iterdir():
            if entry.is_file():

                ext = entry.suffix.lower()
                found = False

                for catagory, (files, extensions) in self.catagories.items():
                    # print(ext)
                    if ext in extensions:
                        files.append(entry.name)
                        found = True
                        break

                if not found:
                    self.catagories["Documents"][0].append(entry.name)
        
        for catagory, (files, extensions) in self.catagories.items():
            if files:
                self.results.append(f"{catagory}: {len(files)}")

        total = sum(len(files) for files, _ in self.catagories.values())
        self.results.append(f"Total: {total}")

        return "\n".join(self.results)

    def orgonaizeFolder(self, folder_path):

        if self.delete_empty_folders:
            folders = [p for p in folder_path.iterdir() if p.is_dir()]
            for folder in folders:
                is_empty = not any(folder.iterdir())
                if is_empty:
                    delete_empty_folder(folder)

        for catagory, (files, extensions) in self.catagories.items():
            if files:
                target_folder = folder_path / catagory
                try:
                    target_folder.mkdir(exist_ok=False)
                    move_files(folder_path, target_folder, files)
                except FileExistsError:
                    print(f"{catagory} folder already exists")
                    move_files(folder_path, target_folder, files)

        return "\n".join("Successful!!")

