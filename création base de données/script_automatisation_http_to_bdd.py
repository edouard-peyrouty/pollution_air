import script_donnes_csv_data
import script_requete_download_http

# attention verifier nom de la base de données

######################################################################
#
#           # READ ME
#   lancer la fonction choix avec le cas choisis et les paramètres de la date
#
#   CASE :  1 = 1 jour 
#           2 = 1 mois
#           3 = 1 semaine
#
######################################################################


def choix(case, year, month, day):
    if case == 1:
        script_requete_download_http.download_day(year, month, day)
        script_donnes_csv_data.all_table_add(1, year, month, day)
    elif case == 2: 
        script_requete_download_http.month_download(year, month)
        script_donnes_csv_data.all_table_add(2, year, month, day)
    elif case == 3: 
        script_requete_download_http.download_week(year, month, day)
        script_donnes_csv_data.all_table_add(3, year, month, day)


if __name__=='__main__':

    case = 2
    year = 2023
    month = 9
    day = 1
    
    choix(case, year, month, day)