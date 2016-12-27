import os
import shutil

path = "<src_path>"
src_folders = os.listdir(path)

for folder_name in src_folders:
    src_files = os.listdir(path+"\\"+folder_name)
    for src_file in src_files:
        file_path = path+"\\"+folder_name+"\\"+src_file
        if (os.path.isfile(file_path)):
            shutil.copy(file_path, path)