import csv
import sqlite3
from datetime import datetime
import os 


####
#
#   Ce fichier ajout des données dans la base de données GEOD'AIR avec plusieurs fonctionnalité 
#
####

##############################################################################################
# Variable global || Si changement ne pas oublier de supprimer les anciennes données créee
##############################################################################################


# Si changement de base de données, changer la variable global DATABASE_NAME
DATABASE_NAME = 'base_de_donnee_air_test.db'
# Si changement de fichier de sauvegarde, changer la variable global SAVE_NAME
SAVE_NAME = 'fichier_save_name.csv'

##############################################################################################
# Lecture fichiers csv   
##############################################################################################

def read_csv(name):
    tab = []
    with open(name, 'r', newline='', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter=';')
        for ligne in lecteur_csv:
            tab.append(ligne)
    return tab

##############################################################################################
#  Ajout des données du fichier csv dans un tableau
##############################################################################################

def add_values_table(tab, tab_table, tab_final, tab_selec):

    # Parcours d'une ligne du fichier CSV
    for lignes in tab: 
        # Exctraction des champs pour une table précis dans un tableau
        for number in tab_table:
            values = lignes[number]
            tab_selec.append(values)
        # Ajout dans le tableau final pour l'ajout des données dans la table
        tab_final.append(tab_selec)
        # reinitialisatoin du tableau pour faire une nouvelle ligne
        tab_selec = []

##############################################################################################
# Création de tableaux tuples  --> pour ajout dans le base de données avec une REQUETE 
##############################################################################################

def selection(name_csv, selection_tables):

    tab = read_csv(name_csv)
    tab_selec = []
    tab_final = []

    ### selection des champs
    tab_mesure = [0, 1, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    tab_organisme = [2]
    tab_polluant = [8]
    tab_site = [5, 6, 7, 9, 3]
    tab_zas = [3, 4, 2]

    if (selection_tables == 1):
        add_values_table(tab, tab_mesure, tab_final, tab_selec)
    if (selection_tables == 2):
        add_values_table(tab, tab_organisme, tab_final, tab_selec)
    if (selection_tables == 3):
        add_values_table(tab, tab_polluant, tab_final, tab_selec)
    if (selection_tables == 4):
        add_values_table(tab, tab_site, tab_final, tab_selec)
    if (selection_tables == 5):
        add_values_table(tab, tab_zas, tab_final, tab_selec)

    del tab_final[0]

    # mise en forme des sous tableau en forme de tuples ma compréhension
    sous_tableau_tuples = [tuple(ligne) for ligne in tab_final]

    return sous_tableau_tuples

##############################################################################################
# changement de type sur les données mesures pour le bon format 
##############################################################################################

def types_tuples_mesure(table_final):
    """ Cette fonction permet de transformer les types qui ne sont pas des str pour les avoir sous le bon format dans la table mesure (La seul qui a des types hors str)"""
    typed_table = []

    for elements in table_final:

        debut = str(elements[0])
        fin = str(elements[1])
        # transformation des types des dates au format iso 8601
        debut = datetime.strptime(debut, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        fin = datetime.strptime(fin, '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        valeur = float(elements[9]) if elements[9] else 0.0
        valeur_brute = float(elements[10]) if elements[10] else 0.0
        if valeur <= 0.0:
            valeur = 0.01
        if valeur_brute <= 0.0: 
            valeur_brute = 0.01

        # création du tuple d'une ligne de données 
        typed_row = (
            debut,  # debut
            fin,  # fin
            str(elements[2]),  # codeSite
            str(elements[3]),  # nomPolluant
            str(elements[4]),  # discriminant
            str(elements[5]),  # reglementaire
            str(elements[6]),  # typeEvaluation
            str(elements[7]),  # procedureMesure
            str(elements[8]),  # typeValeur
            valeur,
            valeur_brute,
            str(elements[11]),  # unite
            str(elements[12]),  # tauxSaisie
            str(elements[13]),  # couvertureTemporelle
            str(elements[14]),  # couvertureDonnees
            str(elements[15]),  # codeQualite
            int(elements[16])
        )
        typed_table.append(typed_row)

    return typed_table

##############################################################################################
# ajout des noms dans le fichier sauvegarde.    
##############################################################################################

def write_fichier_save(name_tab):
    with open(SAVE_NAME, 'a', newline='', encoding='utf-8') as fichier:
        writer = csv.writer(fichier, delimiter=';') 
        writer.writerows([[name] for name in name_tab])

    print('Ligne écrite avec succès dans : ', SAVE_NAME)

##############################################################################################
# Création du nom des fichiers 
##############################################################################################  
    
def test_day(day, year, month):
    """ Définition du nom de fichier à télécharger """
    return f"save/FR_E2_{year}-{month:02d}-{day:02d}.csv"


def tab_crea_auto(case, year, number_month, day_start):
    """ Création des noms pour l'automatisation de l'ajout des données dans les tables/bases de données """
    # tableau qui sauvegarde les noms des fichiers 
    tab = []

    # verification des mois pair impair et fevrier 
    if number_month == 2: 
        max_jours = 28
    elif number_month in [1, 3, 5, 7, 8, 10, 12]:
        max_jours = 31
    else:
        max_jours = 30

    if case == 1: 
        name = test_day(day_start, year, number_month)
        tab.append(name)
    elif case == 2: 
        for i in range(1, max_jours + 1):
            name = test_day(i, year, number_month)
            tab.append(name)
    elif case == 3:
        for i in range(1, 7 + 1):
            day = i + day_start - 1
            name = test_day(day, year, number_month)
            tab.append(name)

    #####################################################################################################################################################################        
    #return tab
    ############################### Ligne à supprimer si il n'y a pas de test


    ############
    #  ouverture du fichier de sauvegarde pour verifier si un fichier csv à deja été mis dans la base de données            
    ############
                
    # Créer le fichier de sauvegarde s'il n'existe pas
    if not os.path.exists(SAVE_NAME):
        open(SAVE_NAME, 'w').close()

    # tableau qui sauvegarde le nom des fichiers deja upload dans la bdd            
    tab_save = []

    # Lecture du fichier de sauvegarde
    with open(SAVE_NAME, 'r', newline='', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier, delimiter=';')
        for ligne in lecteur_csv:
            tab_save.append(ligne)

    # Liste temporaire pour stocker les noms à conserver
    temp_tab = []

    # Parcourir les noms
    for i in range(len(tab)):
    # Vérifier si le nom est dans la liste de sauvegarde
        nom_trouve = False
        for name in tab_save:
            if name[0] == tab[i]:
                nom_trouve = True
                break
    
        # Si le nom n'a pas été trouvé, l'ajouter à la liste temporaire
        if not nom_trouve:
            temp_tab.append(tab[i])

   
    # Réaffectation de la liste tab avec la liste temporaire filtrée
    if tab_save != []:
        tab = temp_tab

    print("Données ajouté dans la bdd : ", tab)

    # Ecriture des fichier qui viennt d'être ajouté dans le fichier de sauvegarde
    write_fichier_save(tab)

    return tab




##############################################################################################
# insertion des données dans les tables avec 3 cas possibles.  
##############################################################################################


def add_data_to_table(tab, table_name, csv_type):

    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Définir les requêtes d'insertion en fonction de la table
    if table_name == "Mesure":
        insert_query = '''
            INSERT OR IGNORE INTO Mesure (
                debut, fin, codeSite, nomPolluant, discriminant,
                reglemantaire, typeEvaluation, procedureMesure, typeValeur,
                valeur, valeurBrute, unite, tauxSaisie, couvertureTemporelle,
                couvertureDonnees, codeQualite, validite
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    elif table_name == "Organisme":
        insert_query = '''
            INSERT OR IGNORE INTO Organisme (nomOrganisme) VALUES (?)
        '''
    elif table_name == "Polluant":
        insert_query = '''
            INSERT OR IGNORE INTO Polluant (nomPolluant) VALUES (?);
        '''
    elif table_name == "Site":
        insert_query = '''
            INSERT OR IGNORE INTO Site (codeSite, nomSite, typeImplantation, typeInfluence, codeZas) VALUES (?, ?, ?, ?, ?);
        '''
    elif table_name == "Zas":
        insert_query = '''
            INSERT OR IGNORE INTO Zas (codeZas, nomZas, nomOrganisme) VALUES (?, ?, ?);
        '''
    else:
        print("Table non prise en charge.")
        return

    for csv_name in tab:
        # Sélectionner les données à partir du fichier CSV
        tab_data = selection(csv_name, csv_type)
        if csv_type == 1:
            tab_data = types_tuples_mesure(tab_data)
        # Insérer les données dans la base de données
        cursor.executemany(insert_query, tab_data)

    print(f"Données pour la table {table_name} ajoutées ! ")
    
    conn.commit()
    conn.close()




#############################################################################################
    ### Different cas : ##### 1 = 1 jour ##### 2 = 1 mois ##### 3 = 7 jours ##
    ## ajout des données des 5 tables
#############################################################################################

def all_table_add(case, year, month, day):
    tab = tab_crea_auto(case, year, month, day)

    add_data_to_table(tab, "Mesure", 1)
    add_data_to_table(tab, "Organisme", 2)
    add_data_to_table(tab, "Polluant", 3)
    add_data_to_table(tab, "Site", 4)
    add_data_to_table(tab, "Zas", 5)

    delete_file()

##############################################################################################
# supprésion des fichiers sur l'ordinateur présent dans la bdd
##############################################################################################

def delete_file():

    try:
        # Liste tous les fichiers dans le répertoire
        files = os.listdir('save')

        for file_name in files:
            try:
                # Construction du chemin complet du fichier
                file_path = os.path.join('save', file_name)

                # Vérification si le chemin est un fichier (et non un sous-répertoire)
                if os.path.isfile(file_path):
                    # Suppression du fichier
                    os.remove(file_path)
                    print(f"Fichier {file_name} supprimé avec succès.")
                else:
                    print(f"{file_name} n'est pas un fichier et n'a pas été supprimé.")
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier {file_name}: {str(e)}")

        print("Suppression des fichiers terminée.")
    except Exception as e:
        print(f"Erreur lors de la récupération de la liste des fichiers : {str(e)}")