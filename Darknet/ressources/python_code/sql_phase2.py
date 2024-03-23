import sqlite3 as sql
import pandas as pd
import datetime

# create the 'url_filter' table
def createSqliteTable(connexion):
    c = connexion.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS url_filter (
        url TEXT,
        title TEXT,
        description TEXT,
        date_analyse,
        statut TEXT,
        valeur INT      
    )''')
    connexion.commit()

# add data to the table
def add_db(url, title, description, statut, valeur):
    data = [url,title, description, datetime.datetime.now(), statut, valeur]
    connexion = sql.connect("../../results/darknet_url.db")
    c = connexion.cursor()                                                                                           # [url, title, description, str(datetime.datetime.now()), statut]
    c.execute("REPLACE INTO url_filter (url, title, description, date_analyse, statut, valeur) VALUES(?, ?, ?, ?, ?, ?)", data)
    connexion.commit()
    print('\n{} records inserted/replaced to the table.'.format(c.rowcount))
    connexion.close()


