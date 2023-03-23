from PIL import Image

def duplicate_qrcode(email):
    # Taille de l'image à coller
    image_to_paste = Image.open("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/qrcode2.png").resize((610,610))
    #new_image_to_paste = write_on_qrcode(path + "/dossier1/qrcode2_logo.png", name_entreprise)

    # Taille de l'image A4
    a4_width, a4_height = 2480, 3508  # en pixels

    # Calculer la taille d'une image collée
    paste_width = int((a4_width - 50) / 4)  # 10px de marge
    paste_height = int((a4_height - 50) / 5)  # 10px de marge

    # Créer une nouvelle image A4
    a4_image = Image.new('RGB', (a4_width, a4_height), (255, 255, 255))

    # Coller les images sur la nouvelle image A4
    for i in range(5):  # parcourir les rangées
        for j in range(4):  # parcourir les colonnes
            x = 25 + j * paste_width  # 10px de marge
            y = 25 + i * paste_height  # 10px de marge
            a4_image.paste(image_to_paste, (x, y))

    # Enregistrer l'image A4
    a4_image.save("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/autocollant-qrcode.png")