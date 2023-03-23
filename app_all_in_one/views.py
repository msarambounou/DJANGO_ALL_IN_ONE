from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import User_additional, Entreprise_social_media, UserConfirmation, Business_card_social_media, All_social_media, Telephonie, Secteur, Entreprise
import string
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from djangoProject1 import settings
from djangoProject1 import settings
from app_all_in_one.tools_email import email_confirmer_inscription, email_welcome, email_forget_password
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from app_all_in_one.tools_random import generate_random_string, custom_generate_random_string
import os
from app_all_in_one.tools_os import folder_user_bs, folder_entreprise_pl
from app_all_in_one.tools_qrcode import generate_qrcode_bs, generate_qrcode_pl
from app_all_in_one.tools_flyer import generate_flyers
from app_all_in_one.tools_image import duplicate_qrcode
import zipfile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password

#----------------------------------------------------------- HOME -----------------------------------------------------------
def home(request):
    return render(request, '07_Apps/00_Home/home.html')

def infos_plaque(request):
    return render(request, '07_Apps/00_Home/infos_plaque.html')

def infos_business_card(request):
    return render(request, '07_Apps/00_Home/infos_business_card.html')

#------------------------------------------------------- AUTHENTIFICATION -------------------------------------------------------
def inscription(request):
    letters = string.ascii_lowercase
    #random_code = ''.join(random.choice(letters) for i in range(8))

    random_code = random.randrange(10000, 99999)

    if request.method == "POST":
        #genre = request.POST["genre"]
        firstname = request.POST["first_name"].capitalize()
        lastname = request.POST["last_name"].upper()
        email = request.POST["email"].lower()
        password = request.POST["password"]
        password_confirmation = request.POST["confirme_password"]

        if password_confirmation != password:
            messages.error(request, "Mot de passe de confirmation différent du mot de passe")
            return redirect("/inscription/")

        User.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password,
                                 username=email, is_active=0)

        folder_name = str(email + str(random.randrange(10000, 99999)))

        User_additional.objects.create(email=email, job="Inconnu", job_description=" ", folder_path="media/users_media/" + folder_name, path_profil="/media/ressources/inconnu.png")

        UserConfirmation.objects.create(email=email, code_confirmation=random_code)

        folder_user_bs(folder_name)

        generate_qrcode_bs("https://www.instagram.com/itsmams.sb/", folder_name)

        generate_flyers(folder_name)

        duplicate_qrcode(folder_name)

        email_confirmer_inscription(random_code, email, firstname)

        #messages.success(request, "Un code de confirmation vous à été envoyé par email")
        return redirect("/confirmation_inscription/" + email)

    return render(request, '02_Authentification/01_Inscription.html')


def confirmation_inscription(request, email):
    new_user = UserConfirmation.objects.all().get(email=email)
    user = User.objects.all().get(email=email)
    #users = list(User.objects.values_list("username", flat=True))
    if request.method == "POST":
        code_confirmation = request.POST["code_confirmation"]

        if new_user.email == email and new_user.code_confirmation == code_confirmation:
            User.objects.filter(username=email).update(is_active=1)

            email_welcome(email, str(user.first_name))

            #messages.success(request,"Votre compte à été créer !")
            return redirect("/connexion/")
        else:
            #messages.error(request, "Code de confirmation incorrecte")
            return redirect("/confirmation_inscription/"+email)

    return render(request, '02_Authentification/02_Confirmation_inscription.html', {
        "email":email
    })

def connexion(request):
    if request.method == "POST":
        email = request.POST["email"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            messages.success(request, "Connecté(e) !")
            return redirect("/")
        else:
            messages.error(request, "Email ou mot de passe incorrect")
            redirect("/connexion/")
    return render(request, '02_Authentification/03_Connexion.html')

@login_required(login_url="/connexion/")
def logout(request):
    auth.logout(request)
    messages.error(request, "Déconnecté(e)")
    return redirect('/')

def my_account(request):
    return render(request, '02_Authentification/04_MyAccount.html')

def update_my_account(request):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        firstname = request.POST["new_firstname"].capitalize()
        lastname = request.POST["new_lastname"].upper()

        User.objects.all().filter(id=current_user_id).update(first_name=firstname, last_name=lastname)
        messages.success(request, "Modification réussit !")
        return redirect("/mon_compte/")

    return render(request, '02_Authentification/update/01_Update_Confidentialite.html')

def update_password(request):
    current_user = request.user
    current_user_id = current_user.id

    user = User.objects.get(id=current_user_id)

    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirmation_password = request.POST["confirme_new_password"]

        if user.check_password(current_password):
            if confirmation_password != new_password:
                messages.error(request, "Mot de passe de confirmation différent du mot de passe")
                return redirect("/modifier_mot_de_passe/")

            if user.check_password(new_password):
                messages.error(request, "Utiliser un autre mot de passe")
                return redirect("/modifier_mot_de_passe/")

            User.objects.filter(id=current_user_id).update(password=make_password(new_password))

            messages.success(request, "Votre mot de passe à été changé")
        else :
            messages.error(request, "Le mot de passe actuel est incorrect")
            return redirect("/modifier_mot_de_passe/")

        return redirect("/connexion/")
    return render(request, '02_Authentification/update/02_Update_Password.html')

def input_email_for_code(request):
    all_email = list(User.objects.values_list("username", flat=True))


    if request.method == "POST":
        email = request.POST["email"]

        if email in all_email:
            user = User.objects.all().get(username=email)
            email_forget_password(email, str(user.first_name))

            messages.success(request, "Vous allez recevoir un email pour changer votre mot de passe.")
            return redirect("/mot_de_passe_oublie/")

    return render(request, '02_Authentification/update/04_input_email_for_send_code.html')

def forget_password(request, email):

    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirmation_password = request.POST["confirme_new_password"]

        if confirmation_password != new_password:
            messages.error(request, "Mot de passe de confirmation différent du mot de passe")
            return redirect("/changer_mot_de_passe_oublie/" + str(email))

        User.objects.all().filter(username=email).update(password=make_password(new_password))

        messages.success(request, "Mot de passe modifié avec succès !")
        return redirect("/connexion/")

    return render(request, '02_Authentification/update/03_Update_Forget_password.html')
#------------------------------------------------------- APP : BUSINESS CARD -------------------------------------------------------
def manage_profile(request):
    current_user = request.user
    current_user_id = current_user.id

    user = User.objects.all().get(id=current_user_id)

    profil = User_additional.objects.all().get(email=user.email)

    return render(request, '07_Apps/Business_card/manage_profil.html', {
        "profil": profil
    })

def update_profil(request):
    current_user = request.user
    current_user_id = current_user.id

    user = User.objects.all().get(id=current_user_id)

    profil = User_additional.objects.all().get(email=user.email)

    if request.method == "POST":
        job = request.POST['job']
        description = request.POST['description']
        image = request.FILES['image']

        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        image_url = fss.url(file)
        print(image_url)

        if image is None:
            User_additional.objects.filter(email=profil.email).update(job=job, job_description=description)
        else:
            User_additional.objects.filter(email=profil.email).update(job=job, job_description=description, path_profil=image_url)

        return redirect("/gerer_mon_profile/")

    return render(request, '07_Apps/Business_card/update_profil.html', {
        "profil":profil
    })

def manage_business_card(request):
    current_user = request.user
    current_user_id = current_user.id

    list_user_social_media = Business_card_social_media.objects.values_list("name", flat=True).filter(
        id_user=current_user_id)

    active_social_media = list(list_user_social_media)

    all_social_media = All_social_media.objects.exclude(name__in=active_social_media)

    bs_social_media = Business_card_social_media.objects.all().filter(id_user=current_user_id)
    len_bs_social_media = len(bs_social_media)
    print("len_bs_social_media :", len_bs_social_media)

    telephonie = Telephonie.objects.all()

    return render(request, '07_Apps/Business_card/manage_business_card.html', {

        'all_social_media': all_social_media,
        'bs_social_media':bs_social_media,
        'len_bs_social_media':len_bs_social_media,
        "telephonie": telephonie
    })

def add_social_media_bs(request):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        name = request.POST["name"]
        link = request.POST["link"]
        country = request.POST["country"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        full_phone_number = "0000"

        if (link == "" and phone_number == "" and email == ""):

            return redirect("/gerer_ma_smart_business_card/")

        elif name == "WhatsApp":
            full_phone_number = country + phone_number
            link = "https://wa.me/" + full_phone_number

        elif name == "Email":
            link = email

        social_media = All_social_media.objects.all().get(name=name)

        Business_card_social_media.objects.create(
            path_logo=social_media.path_logo,
            name=name,
            id_user=current_user_id,
            link=link,
            phone_number=full_phone_number,
            indicateur=country,
        )

        return redirect("/gerer_ma_smart_business_card/")

    return render(request, '07_Apps/Business_card/add_social_media.html')

def display_from_business_card(request):
    current_user = request.user
    current_user_id = current_user.id

    user = User.objects.all().get(id=current_user_id)

    profil = User_additional.objects.all().get(email=user.email)

    social_media = Business_card_social_media.objects.all().filter(
        id_user=current_user_id
    )

    return render(request, '07_Apps/Business_card/display_social_media.html', {
        'social_media':social_media,
        "profil":profil
    })

def update_social_media_bs(request, id_social_media):

    social_media = Business_card_social_media.objects.all().get(
        id=id_social_media
    )

    if request.method == "POST":
        if social_media.name == "WhatsApp":
            indicateur = request.POST["country"]
            phone_number = request.POST["phone_number"]

            link = "https://wa.me/" + indicateur +  phone_number

            Business_card_social_media.objects.all().filter(id=id_social_media).update(phone_number=phone_number, indicateur=indicateur, link=link)
        else:
            link = request.POST["link"]

        Business_card_social_media.objects.all().filter(id=id_social_media).update(link=link)

        return redirect("/gerer_ma_smart_business_card/")


    return render(request, '07_Apps/Business_card/update_social_media_bs.html', {
        "social_media":social_media
    })

def delete_social_media_bs(request, id_social_media):

    social_media = Business_card_social_media.objects.all().get(
        id=id_social_media
    )

    if request.method == "POST":

        Business_card_social_media.objects.all().filter(id=id_social_media).delete()

        return redirect("/gerer_ma_smart_business_card/")


    return render(request, '07_Apps/Business_card/delete_social_media_bs.html', {
        "social_media":social_media
    })

#------------------------------------------------------- APP : PLAQUE -------------------------------------------------------

def manage_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    secteurs = Secteur.objects.all()
    entreprises = Entreprise.objects.all().filter(id_user=current_user_id, statut=1)
    len_entreprises = len(entreprises)

    return render(request, '07_Apps/Plaque/manage_entreprise.html', {
        "secteurs":secteurs,
        "entreprises":entreprises,
        "len_entreprises":len_entreprises
    })

def add_entreprise(request):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        name_entreprise = request.POST['name_entreprise'].capitalize()
        secteur = request.POST['secteur'].capitalize()

        Entreprise.objects.create(nom_entreprise=name_entreprise, secteur=secteur, id_user=current_user_id, statut=1)

        user = User.objects.all().get(id=current_user_id)
        user_add = User_additional.objects.all().get(email=str(user.email))

        folder_entreprise_pl(str(user_add.folder_path), name_entreprise.replace(" ", ""))
        generate_qrcode_pl("https://www.instagram.com/itsmams.sb/", str(user_add.folder_path), name_entreprise.replace(" ", ""))

        return redirect("/gerer_mes_entreprises/")

    return render(request, '03_Modal/add_entreprise.html')

def manage_rs_plaque(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    list_user_social_media = Entreprise_social_media.objects.values_list("name", flat=True).filter(
        id_user=current_user_id, id_entreprise=id_entreprise)

    active_social_media = list(list_user_social_media)

    all_social_media = All_social_media.objects.exclude(name__in=active_social_media)

    bs_social_media = Entreprise_social_media.objects.all().filter(id_user=current_user_id, id_entreprise=id_entreprise)
    len_bs_social_media = len(bs_social_media)

    entreprise = Entreprise.objects.all().get(id=id_entreprise)

    telephonie = Telephonie.objects.all()

    return render(request, '07_Apps/Plaque/mange_social_media.html', {

        'all_social_media': all_social_media,
        'bs_social_media': bs_social_media,
        'len_bs_social_media': len_bs_social_media,
        "telephonie": telephonie,
        "id_entreprise": id_entreprise,
        "nom_entreprise": entreprise.nom_entreprise
    })

def add_social_media_plaque(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    if request.method == "POST":
        name = request.POST["name"]
        link = request.POST["link"]
        country = request.POST["country"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]

        full_phone_number = "0000"

        if (link == "" and phone_number == "" and email == ""):

            return redirect("/gerer_ma_smart_business_card/")

        elif name == "WhatsApp":
            full_phone_number = country + phone_number
            link = "https://wa.me/" + full_phone_number

        elif name == "Email":
            link = email

        social_media = All_social_media.objects.all().get(name=name)

        Entreprise_social_media.objects.create(
            path_logo=social_media.path_logo,
            name=name,
            id_user=current_user_id,
            link=link,
            phone_number=full_phone_number,
            id_entreprise=id_entreprise,
            indicateur=country
        )

        return redirect("/gerer_mes_reseaux_sociaux/" + str(id_entreprise))

    return render(request, '07_Apps/Business_card/add_social_media.html')

def display_from_plaque(request, id_entreprise):
    current_user = request.user
    current_user_id = current_user.id

    social_media = Entreprise_social_media.objects.all().filter(
        id_user=current_user_id, id_entreprise=id_entreprise
    )

    return render(request, '07_Apps/Plaque/display_entreprise_social_media.html', {
        'social_media':social_media,
    })

def update_social_media_pl(request, id_social_media):

    social_media = Entreprise_social_media.objects.all().get(
        id=id_social_media
    )

    if request.method == "POST":
        if social_media.name == "WhatsApp":
            indicateur = request.POST["country"]
            phone_number = request.POST["phone_number"]

            link = "https://wa.me/" + indicateur +  phone_number

            Entreprise_social_media.objects.all().filter(id=id_social_media).update(phone_number=phone_number, indicateur=indicateur, link=link)
        else:
            link = request.POST["link"]

        Entreprise_social_media.objects.all().filter(id=id_social_media).update(link=link)

        return redirect("/gerer_mes_reseaux_sociaux/" + str(social_media.id_entreprise))


    return render(request, '07_Apps/Plaque/update_social_media.html', {
        "social_media":social_media
    })

def delete_social_media_pl(request, id_social_media):

    social_media = Entreprise_social_media.objects.all().get(
        id=id_social_media
    )

    if request.method == "POST":

        Entreprise_social_media.objects.all().filter(id=id_social_media).delete()

        return redirect("/gerer_mes_reseaux_sociaux/" + str(social_media.id_entreprise))


    return render(request, '07_Apps/Plaque/delete_social_media.html', {
        "social_media":social_media
    })



def delete_entreprise(request, id_entreprise):

    entreprise = Entreprise.objects.all().get(id=id_entreprise)

    if request.method == "POST":
        entreprise.delete()

        return redirect("/gerer_mes_entreprises/")

    return render(request, '07_Apps/Plaque/delete_entreprise.html',{
        "entreprise": entreprise
    })

def update_entreprise(request, id_entreprise):

    entreprise = Entreprise.objects.all().get(id=id_entreprise)
    all_secteur = Secteur.objects.all().distinct().exclude(libelle_secteur=entreprise.secteur)


    if request.method == "POST":
        name_entreprise = request.POST['name_entreprise'].capitalize()
        secteur = request.POST['secteur'].capitalize()

        Entreprise.objects.all().filter(id=id_entreprise).update(
            nom_entreprise= name_entreprise,
            secteur = secteur
        )

        return redirect("/gerer_mes_entreprises/")

    return render(request, '07_Apps/Plaque/update_entreprise.html', {
        'entreprise': entreprise,
        "all_secteur" : all_secteur
    })


#-------------------------------------- OS OPERATION --------------------------------------
def download_bc_folder(request, email):

    folder_path = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier1"

    zip_filename = folder_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip.write(file_path, os.path.relpath(file_path, folder_path))
    response = HttpResponse(open(zip_filename, 'rb').read())
    response['Content-Disposition'] = 'attachment; filename="mes_ressources.zip"'
    return response

def download_pl_folder(request, email):

    folder_path = "/Users/mamadousarambounou/Desktop/projet/djangoProject1/media/users_media/" + email + "/dossier2"

    zip_filename = folder_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip.write(file_path, os.path.relpath(file_path, folder_path))
    response = HttpResponse(open(zip_filename, 'rb').read())
    response['Content-Disposition'] = 'attachment; filename="mes_ressources.zip"'
    return response


#-------------------------------------- ABONNEMENTS --------------------------------------
def abonnement(request):
    return render(request, '08_Abonnements/abonnement_page1.html')

def abonnement2(request):
    return render(request, '08_Abonnements/abonnement_page2.html')