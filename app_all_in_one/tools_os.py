import os
import string
import random

def folder_user_bs(email):

    users_folder_name = str(email)
    users_folder_path = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + users_folder_name

    os.mkdir(os.path.join("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/",users_folder_path))
    os.mkdir(os.path.join(users_folder_path, "dossier1"))

def folder_entreprise_pl(path, nom_entreprise):
    users_folder_path = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/" + path + "/"
    os.mkdir(os.path.join(users_folder_path, nom_entreprise))





#------------------------------- TEST -------------------------------
def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        new_directory_path = directory_path + "_" + random_string
        os.makedirs(new_directory_path)
        print(f"Directory '{directory_path}' already exists. New directory '{new_directory_path}' created.")