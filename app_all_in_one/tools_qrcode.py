import segno
from PIL import Image
from .models import User_qrcode

def generate_qrcode_bs(url_redirection, email):
    qrcode = segno.make_qr(url_redirection, error='H')

    path_qrcode_folder = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/"

    qrcode.save(path_qrcode_folder + "qrcode1.png", dark='white', light='black', scale=100)
    qrcode.save(path_qrcode_folder + "qrcode2.png", scale=100)

def generate_qrcode_pl(url_redirection, path, nom_entreprise):
    qrcode = segno.make_qr(url_redirection, error='H')

    #path_qrcode_folder = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/" + nom_entreprise
    path_qrcode_folder = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/" + path + "/" + nom_entreprise

    qrcode.save(path_qrcode_folder + "/qrcode1.png", dark='white', light='black', scale=100)
    qrcode.save(path_qrcode_folder + "/qrcode2.png", scale=100)