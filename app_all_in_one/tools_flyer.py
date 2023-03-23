from PIL import Image


def generate_flyers(email):
    flyer1 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/djangoProject1/app_all_in_one/static/image/flyers/flyer1.png")
    flyer2 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/djangoProject1/app_all_in_one/static/image/flyers/flyer2.png")
    flyer3 = Image.open(r"/Users/mamadousarambounou/Desktop/projet/djangoProject1/app_all_in_one/static/image/flyers/flyer3.png")

    # Récupération des dimensions actuelles
    width, height = flyer1.size

    # Calcul des nouvelles dimensions
    new_width = width / 1.5
    new_height = height / 2.1

    qrcode = Image.open(r"/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/qrcode2.png").resize((int(new_width), int(new_height)))

    flyer_width, flyer_height = flyer1.size
    qrcode_width, qrcode_height = qrcode.size
    position = ((flyer_width - qrcode_width) // 2, (flyer_height - qrcode_height) // 2)

    flyer1.paste(qrcode, position)
    flyer2.paste(qrcode, position)
    flyer3.paste(qrcode, position)

    flyer1.save("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/flyer1.png")
    flyer2.save("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/flyer2.png")
    flyer3.save("/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1/flyer3.png")