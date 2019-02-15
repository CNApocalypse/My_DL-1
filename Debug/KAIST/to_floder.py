import os,sys,shutil
path = "char/"
def create_new_folder(folder_name):
    os.makedirs(path+folder_name)

def move_files(to_path,file_name):
    try:
        shutil.move(path+file_name,path+to_path+file_name)
    except FileNotFoundError:
        create_new_folder(to_path)
        shutil.move(path+file_name,path+to_path+file_name)
def main():
    file_list = []
    for _,_,files in os.walk(path):
        file_list = files
    
    for fname in file_list:
        move_files(fname[:1]+'/',fname)

if __name__ =="__main__":
    main()

