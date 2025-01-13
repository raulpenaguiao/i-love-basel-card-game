import shutil

for i in range(10, 201):
    shutil.copy("resources//imgs//icons//nia.jpg", f"resources//imgs//cards//card{i}.jpg")