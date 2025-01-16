import shutil

for i in range(201):
    shutil.copy("resources//imgs//icons//nia.jpg", f"resources//imgs//cards//card" + f'{i:03d}' + ".jpg")