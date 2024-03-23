from flask import Flask, render_template
import sqlite3
import os
import pandas as pd
from graphiques import *

# Déclaration d'application Flask
app = Flask(__name__)

# Configuration pour servir les fichiers statiques
app.static_folder = 'static'

# Nom de la base de données SQLite
DATABASE = "base_de_donnee.db"

# Chemin relatif vers la base de données
db_path = os.path.join(os.path.dirname(__file__), 'data', DATABASE)

def requete_sql(requete):
    """Renvoie le résultat d'une requete sql passée en paramètre"""
    conn = sqlite3.connect(db_path)
    resultat = pd.read_sql_query(requete, conn)
    conn.close()
    return resultat

# Route pour la page d'accueil
@app.route('/')
def accueil():
    # recupérer la liste des polluants
    requete = "SELECT * FROM Polluant"
    polluants = requete_sql(requete)
    # afficher la page
    return render_template('index.html',polluants=polluants)

@app.route('/organisme/<nom_organisme>')
def organisme(nom_organisme):
    # on récupère la liste des zas dans l'organisme
    requete = f"SELECT * FROM Zas WHERE nomOrganisme = '{nom_organisme}'"
    zas = requete_sql(requete)

    return render_template("organisme.html",organisme=nom_organisme,zas=zas)

@app.route("/zone/<echelle>/<zone_id>", methods=['POST','GET'])
def zone(echelle,zone_id):
    if echelle == "Organisme":
        noms = {"sous_zone":"Zas","zone_id":"nomOrganisme","nom_zone":"nomOrganisme"}
    elif echelle == "Zas":
        noms = {"sous_zone":"Site","zone_id":"codeZas","nom_zone":"nomZas"}
    elif echelle == "Site":
        noms = {"sous_zone":"Site","zone_id":"codeSite","nom_zone":"nomSite"}

    # on récupère la liste des sous-zones dans la zone
    requete = f"SELECT * FROM {noms['sous_zone']} WHERE {noms['zone_id']} = '{zone_id}'"
    sous_zones = requete_sql(requete)

    # on récupere la liste des polluants
    requete = "SELECT * FROM Polluant"
    polluants = requete_sql(requete)["nomPolluant"].tolist()

    # on récupère les informations du formulaire
    mois,jour,polluant,seuil = get_form()

    # on récupère les mesures d'un ensemble de dates dans la zas
    requete = f"""
    SELECT * FROM Mesure 
    JOIN Site ON Mesure.codeSite = Site.codeSite
    JOIN Zas ON Site.codeZas = Zas.codeZas
    WHERE {noms['sous_zone']}.{noms['zone_id']} = '{zone_id}'
    AND debut LIKE '%-{mois}-{jour}%' """
    mesures = requete_sql(requete)

    # on récupère le nom de la zone
    nom_zone = mesures.at[1,noms["nom_zone"]]

    # on genere un graphique de l'évolution de la concentration de polluant
    courbe = tracer_courbe(mesures,polluant,jour,int(mois)-1)

    # on genere un histogramme des valeurs moyennes des différenst polluants
    histogramme = tracer_histogramme(mesures,jour,int(mois)-1)

    # on filtre les mesures dépassant le seuil et concernant le polluant selectionné
    depasse_seuil = mesures.query(f"nomPolluant == '{polluant}'")
    depasse_seuil = depasse_seuil.query(f"valeur > {seuil}")
    # on ne garde que les colones que l'on souhaite afficher 
    depasse_seuil = depasse_seuil[["valeur","debut","nomSite","nomZas","nomOrganisme","nomPolluant"]]
    # on ordonne par valuer croissante
    depasse_seuil = depasse_seuil.sort_values(by="valeur", ascending=False)
    
    return render_template("zone.html",nom_zone=nom_zone,sous_zones=sous_zones,sous_echelle=noms["sous_zone"],echelle=echelle,zone_id=zone_id,mois=MOIS,polluants=polluants,courbe=courbe,histogramme=histogramme,depasse_seuil=depasse_seuil[:10],seuil=seuil)

if __name__ == '__main__':
    app.run(debug=True)    