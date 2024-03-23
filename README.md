Ce projet est une application web dynamique qui permet de visualiser les données sur la pollution de l'air récolter par les différents organismes de mesure de la qualité de l'air en France.
Pour cela, il faut dans un premier temps créer la base de données en exécutant les scripts du fichier base_de_données :
- créer le fichier base_de_donnee_air.bd et le placer dans le fichier base_de_données
- exécuter le script script_creation_bdd
- exécuter le script script_automatisation_http_to_bdd
Dans un deuxième temps, il faut copier le fichier base_de_donnee_air.bd dans le dossier data du dossier application_web et exécuter le fichier app.py et vous accèderez à une interface web vous permettant à l'aide d'une carte interactive de sélectionner une zone géographique sur laquelle vous obtiendrez différentes informations sur la qualité de l'air.
