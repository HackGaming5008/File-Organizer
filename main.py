
####################### IMPORTS ##################

import os 
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

# Modes
delete_empty_folders = False
move_enabled = False

#################### FUNCTIONS ###################


def move_files(src, dist, files):
    if files:
        for file in files:
            shutil.move(os.path.join(src, file), os.path.join(dist, file))
            print(f"Moved {file}")
    else:
        print(f"No files to move in {dist}")

def join_path(folder, file):
    return os.path.join(folder, file)

def delete_empty_folder(folder):
    try:
        os.rmdir(folder)
        print(f"Deleted empty folder: {folder.name}")
    except OSError:
        print(f"Could not delete folder: {folder.name} (not empty)")


##################### MAIN ######################

def functionMain(folder_path):

    catagories = {
        "Images": [[], image_ext],
        "Zips": [[], zip_ext],
        "Videos": [[], vid_ext],
        "Music": [[], music_ext],
        "Code": [[], code_ext],
        "PDFs": [[], pdf_ext],
        "Docx": [[], docx_ext],
        "Documents": [[], []]
    }

    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():

                ext = os.path.splitext(entry.name)[1].lower()

                found = False

                for catagory, (files, extensions) in catagories.items():
                    # print(ext)
                    if ext in extensions:
                        files.append(entry.name)
                        found = True
                        break

                if not found:
                    catagories["Documents"][0].append(entry.name)

    if delete_empty_folders:
        folders = [p for p in folder_path.iterdir() if p.is_dir()]
        for folder in folders:
            with os.scandir(folder) as entries:
                entries = list(entries)
                if not entries:
                    delete_empty_folder(folder)




    for catagory, (files, extensions) in catagories.items():
        if move_files:
            if files:
                try:
                    os.mkdir(join_path(folder_path, catagory))
                    move_files(folder_path, join_path(folder_path, catagory), files)
                except FileExistsError:
                    print(f"{catagory} folder already exists")
                    move_files(folder_path, join_path(folder_path, catagory), files)

        print(f"{catagory}: {len(files)}")

    # print(f"Total: {len(images) + len(zips) + len(videos) + len(documents)}")
    total = sum(len(files) for files, _ in catagories.values())
    print(f"Total: {total}")



if __name__ == "__main__":
    functionMain(path)
    print(path)