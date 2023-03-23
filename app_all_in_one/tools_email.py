from django.core.mail import send_mail
from django.template.loader import render_to_string
from djangoProject1 import settings

def email_confirmer_inscription(random_code, user_email, user_firstname):

    # contexte contenant le code à inclure dans l'e-mail
    contexte = {'code': random_code,
                'user_name': user_firstname
                }

    # génération du contenu HTML à partir du modèle et du contexte
    html_contenu = render_to_string('04_Email/send_inscription_code.html', contexte)

    # détails de l'e-mail
    destinataire = [user_email]
    sujet = 'Confirmation inscription'
    expediteur = settings.EMAIL_HOST_USER

    # envoi de l'e-mail
    send_mail(sujet, '', expediteur, destinataire, html_message=html_contenu)


def email_welcome(user_email, user_firstname):

    # contexte contenant le code à inclure dans l'e-mail
    contexte = {
                'user_name': user_firstname
                }

    # génération du contenu HTML à partir du modèle et du contexte
    html_contenu = render_to_string('04_Email/welcome.html', contexte)

    # détails de l'e-mail
    destinataire = [user_email]
    sujet = 'Bienvenue sur ALL IN ONE !'
    expediteur = settings.EMAIL_HOST_USER

    # envoi de l'e-mail
    send_mail(sujet, '', expediteur, destinataire, html_message=html_contenu)


def email_forget_password(user_email, user_firstname):

    # contexte contenant le code à inclure dans l'e-mail
    contexte = {
        'user_email': user_email,
        'user_name': user_firstname
    }

    # génération du contenu HTML à partir du modèle et du contexte
    html_contenu = render_to_string('04_Email/forget_password.html', contexte)

    # détails de l'e-mail
    destinataire = [user_email]
    sujet = 'Bienvenue sur ALL IN ONE !'
    expediteur = settings.EMAIL_HOST_USER

    # envoi de l'e-mail
    send_mail(sujet, '', expediteur, destinataire, html_message=html_contenu)



