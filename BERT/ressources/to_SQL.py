# Importation des modules
import lxml.html
import pandas as pd
import sqlite3

# Fonction pour creer une database SQLite
def createSqliteTable(connexion):
    
    c = connexion.cursor()
    # création de la table URL
    c.execute('''CREATE TABLE IF NOT EXISTS Results (
        url TEXT,
        title TEXT,
        description TEXT,
        published_day
        
    )''')
    connexion.commit()

# Fonction pour ajouter des données à une database SQLite
def addDataSqliteDatabase(connexion, data):
    
    c = connexion.cursor()
    #insert multiple records in a single query
    c.executemany('''REPLACE INTO Results (url, title, description, date_publication) VALUES (?, ?, ?, ?)''', data)
    connexion.commit()
    print('{} records inserted/replaced to the table.'.format(c.rowcount))


# Nom de la db et connexion
#database = 'Exercice.db'
#connexion = sqlite3.connect(database)

# On créer la db
#createSqliteTable(connexion)

# On ajoute les données
#addDataSqliteDatabase(connexion, data_list)
