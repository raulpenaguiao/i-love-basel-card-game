import os
import re
import shutil



def rename_files(folder_path):
    pattern = re.compile(r'card(\d{3})\.jpg')
    
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            new_number = (number + 500)%1000
            new_filename = f'card{new_number:03}.jpg'
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename)
            shutil.copyfile(old_file, new_file)
            print(f'Renamed {filename} to {new_filename}')

folder_path = 'C:\\Users\\rpenaguiao\\Downloads\\pics_game'
rename_files(folder_path)