import sqlite3

#####
# permet de créer la bdd autant de fois que nécessaire 
#####

# Connexion à la base de données SQLite (ou créez-la si elle n'existe pas)
conn = sqlite3.connect('base_de_donnee_air_test.db')

# Création d'une instance de curseur
cur = conn.cursor()

# Définition du schéma de la table Site
cur.execute('''
    CREATE TABLE IF NOT EXISTS Site (
    codeSite TEXT PRIMARY KEY,
    nomSite TEXT,
    typeImplantation TEXT,
    typeInfluence TEXT,
    codeZas TEXT REFERENCES Zas(codeZas)
    );
''')

# Définition du schéma de la table Zas
cur.execute('''
    CREATE TABLE IF NOT EXISTS Zas (
        codeZas TEXT PRIMARY KEY,
        nomZas TEXT,
        nomOrganisme TEXT REFERENCES Organisme(nomOrganisme)
    );
''')

# Définition du schéma de la table Organisme
cur.execute('''
    CREATE TABLE IF NOT EXISTS Organisme (
        nomOrganisme TEXT PRIMARY KEY
    );
''')

# Définition du schéma de la table Polluant
cur.execute('''
    CREATE TABLE IF NOT EXISTS Polluant (
        nomPolluant TEXT PRIMARY KEY
    );
''')

# Définition du schéma de la table Mesure
cur.execute('''
    CREATE TABLE IF NOT EXISTS Mesure (
        debut DATETIME,
        fin DATETIME,
        codeSite TEXT REFERENCES Site(codeSite),
        nomPolluant TEXT REFERENCES Polluant(nomPolluant),
        discriminant TEXT,
        reglemantaire TEXT,
        typeEvaluation TEXT,
        procedureMesure TEXT,
        typeValeur TEXT,
        valeur REAL,
        valeurBrute REAL,
        unite TEXT,
        tauxSaisie TEXT,
        couvertureTemporelle TEXT,
        couvertureDonnees TEXT,
        codeQualite TEXT,
        validite INTEGER
    );
''')

# Valider et fermer la connexion
conn.commit()
conn.close()
