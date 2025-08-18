import os
import shutil

def copy_static():
    home = "static"
    dest = "public"

    shutil.rmtree(dest)
    os.mkdir("public")
    copy_all(home, dest)

def copy_all(home, dest):
    files = os.listdir(home)
    for file in files:
        path = os.path.join(home,file)
        if os.path.isfile(path):
            shutil.copy(path, dest)
        else:
            if not os.path.exists(os.path.join(dest, file)):
                os.mkdir(os.path.join(dest, file))
            copy_all(os.path.join(home,file), os.path.join(dest, file))
