"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_all_in_one import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
    path("savoir_plus_plaque/", views.infos_plaque),
    path("savoir_plus_business_card/", views.infos_business_card),

#-------------- AUTHENTIFICATION --------------------
    path("inscription/", views.inscription),
    path("confirmation_inscription/<email>", views.confirmation_inscription),
    path("connexion/", views.connexion),
    path("logout/", views.logout, name="logout"),

    path("mon_compte/", views.my_account),
    path("modifier_mon_compte/", views.update_my_account),
    path("modifier_mot_de_passe/", views.update_password),

    path("mot_de_passe_oublie/", views.input_email_for_code),
    path("changer_mot_de_passe_oublie/<email>", views.forget_password),

#-------------- APP : BUSINESS CARD --------------------
    path("gerer_mon_profile/", views.manage_profile),
    path("modifier_mon_profile/", views.update_profil),

    path("gerer_ma_smart_business_card/", views.manage_business_card),
    path("ajouter_reseau_social_bs/", views.add_social_media_bs),
    path("modifier_reseau_sociaux_bs/<int:id_social_media>", views.update_social_media_bs),
    path("supprimer_reseau_sociaux_bs/<int:id_social_media>", views.delete_social_media_bs),

    path("ma_smart_business_card/", views.display_from_business_card),

    path("telecharger_ma_business_card/<email>", views.download_bc_folder),

#-------------- APP : PLAQUE --------------------
    path("gerer_mes_entreprises/", views.manage_entreprise),
    path("ajouter_entreprise/", views.add_entreprise),
    path("modifier_entreprise/<int:id_entreprise>", views.update_entreprise),
    path("supprimer_entreprise/<int:id_entreprise>", views.delete_entreprise),

    path("gerer_mes_reseaux_sociaux/<int:id_entreprise>", views.manage_rs_plaque),
    path("ajouter_reseau_social_plaque/<int:id_entreprise>", views.add_social_media_plaque),
    path("modifier_reseau_sociaux_pl/<int:id_social_media>", views.update_social_media_pl),
    path("supprimer_reseau_sociaux_pl/<int:id_social_media>", views.delete_social_media_pl),

    path("rejoignez-nous/<int:id_entreprise>", views.display_from_plaque),

#-------------- ABONNEMENTS --------------------
    path("nos_abonnement/", views.abonnement),
    path("nos_abonnement2/", views.abonnement2),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
