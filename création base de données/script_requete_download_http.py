import requests


def years(years):
    """ Créer le chemin de l'url 1 par rapport à l'annnée """
    url_final = f"https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/{years}/"
    return url_final

def test_sav():
    """ Fonction test de sauvegarde d'un fichier """
    url_base = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/2023/"
    file_name = "FR_E2_2023-01-01.csv"
    # Téléchargement du fichier
    url_file = url_base + file_name
    response = requests.get(url_file)
    if response.status_code == 200:
        return response.content

def test_day(day, year, month):
    """ Créer l'url 2 par rapport à l'année, mois et jour"""
    return f"FR_E2_{year}-{month:02d}-{day:02d}.csv"


def request_download_choice(file_name, name_path_save, year):
    """
    Défini un telechargement pour une journée de données par rapport au nom
    """
    
    #choix de l'année
    url_base_final = years(year)
    
    # Téléchargement du fichier
    url_file = url_base_final + file_name

    response = requests.get(url_file)

    if response.status_code == 200:
        # Mode d'ouverture 'wb' pour écrire en binaire
        with open(name_path_save, 'wb') as fichier:
            # Écriture du contenu binaire dans le fichier
            fichier.write(response.content)
        print(f"Le fichier {file_name} a été téléchargé avec succès.")
    else:
        print(f"Échec du téléchargement. Statut de la requête : {response.status_code}")


def request_download_simple_file(url_file, name_path_save):
    """
    Base de téléchargement pour l'automatisation de téléchargement de toutes les données
    """

    response = requests.get(url_file)
    
    if response.status_code == 200:
        # Mode d'ouverture 'wb' pour écrire en binaire
        with open(name_path_save, 'wb') as fichier:
            # Écriture du contenu binaire dans le fichier
            fichier.write(response.content)
        print(f"Le fichier {name_path_save} a été téléchargé avec succès.")
    else:
        print(f"Échec du téléchargement. Statut de la requête : {response.status_code}")


def download_day(year, month, day):
    """
    Téléchargement sur 1 jour de données
    """
    url_base_final = years(year)
    file_name = test_day(day, year, month)
    save_name = f"save/{file_name}"
    url_file = f"{url_base_final}{file_name}"
    request_download_simple_file(url_file, save_name)


def download_week(year, month, day_start):
    """
    Téléchargement de toutes les données sur 1 semaines en partant d'un jour choisis
    Gère les erreurs de dépassement de mois 
    """

    url_base_final = years(year)
    last_day_of_month = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month in [4, 6, 9, 11] else 28

    if day_start > last_day_of_month - 6:
        print("Erreur : La date de début et les 6 jours suivants dépassent la fin du mois.")
        return

    for day in range(day_start, day_start + 7):
        file_name = test_day(day, year, month)
        save_name = f"save/{file_name}"
        url_file = f"{url_base_final}{file_name}"
        request_download_simple_file(url_file, save_name)



def month_download(annee, number_month):
    """ Telecharge les données de l'air sur 1 mois complet """

    #choix de l'année
    url_base_final = years(annee)
    jour = 1

    #definition du nombre de jour 
    if number_month == 2: 
        max_jours = 28
    elif number_month in [1, 3, 5, 7, 8, 10, 12]:
        max_jours = 31
    else:
        max_jours = 30

    while jour <= max_jours:
        #définition du file_name 
        file_name = test_day(jour, annee, number_month)
        save_name = "save/" + file_name
        # Téléchargement du fichier
        url_file = url_base_final + file_name
        request_download_simple_file(url_file, save_name)
        jour += 1
   

if __name__ == '__main__':
    #file_name = "FR_E2_2023-01-01.csv" 
    #request_download_choice(file_name, 'save/test2.csv', 2023)

    #month_download(2023, 12)
    #download_week(2023, 1, 1)
    #download_day(2023, 5, 3)
    a = test_sav()
    print(a)
    