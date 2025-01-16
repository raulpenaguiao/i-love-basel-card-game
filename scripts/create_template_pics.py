import shutil

for i in range(500, 701):
    shutil.copy("resources//imgs//icons//nia.jpg", f"resources//imgs//cards//card" + f'{i:03d}' + ".jpg")