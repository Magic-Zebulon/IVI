# Importation des modules
import lxml.html
import pandas as pd
import sqlite3

# Function for creating the sql table
def createSqliteTable(connexion):
    c = connexion.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS url_finder (
        url TEXT,
        title TEXT,
        description TEXT,
        published_day,
        scrape_day,
        code_client,
        code_serveur
    )''')
    connexion.commit()

# Function for adding data to the table 'url_finder'
def addDataSqliteDatabase(connexion, data):
    c = connexion.cursor()
    c.executemany('''REPLACE INTO url_finder (url, title, description, published_day, scrape_day, code_client, code_serveur) VALUES (?, ?, ?, ?, ?, ?, ?)''', data)
    connexion.commit()
    print('{} records inserted/replaced to the table.'.format(c.rowcount))

# method for deleting line breaks
def anti_slashN(connexion): 
    curseur = connexion.cursor()
    champs_a_modifier = ['url', 'title', 'description', 'published_day']       
    for champ in champs_a_modifier:     
        curseur.execute(f"UPDATE url_finder SET {champ} = REPLACE(REPLACE(REPLACE({champ}, '\n', ''), '\r', ''), '\r\n', '')")
    connexion.commit()      

# this method removes excess spaces
def anti_space(connexion):
    curseur = connexion.cursor()
    champs_a_modifier = ['url', 'title', 'description', 'published_day']        
    for champ in champs_a_modifier:     
        curseur.execute(f"UPDATE url_finder SET {champ} = REPLACE(REPLACE(REPLACE({champ}, '  ', ' '), '   ', ' '), '    ', ' ')")
    connexion.commit()      

# this method deletes the string 'Ad' if it is at the beginning of the cell
def anti_Ad(connexion):
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM url_finder WHERE url LIKE 'Ad%'")
    connexion.commit()      

# this method adds the string 'http://' if it is not at the beginning of the cell.
def add_http(connexion):
    curseur = connexion.cursor()
    curseur.execute("SELECT url FROM url_finder WHERE NOT url LIKE 'http://%';")
    rows = curseur.fetchall()
    for row in rows:
        old_url = row[0]  
        new_url = f"http://{old_url}"
        curseur.execute("UPDATE url_finder SET url = ? WHERE url = ?;", (new_url, old_url))
    connexion.commit()

# this method deletes duplicates
def anti_double(connexion):
    curseur = connexion.cursor()
    curseur.execute("""
        DELETE FROM url_finder
        WHERE rowid NOT IN (
            SELECT MAX(rowid)
            FROM url_finder
            GROUP BY url
        );
    """)
    connexion.commit()

# this method calls on all those mentioned above
def Mr_propre(connexion):
    anti_slashN(connexion)
    anti_space(connexion)
    anti_Ad(connexion)
    add_http(connexion)
    anti_double(connexion)
    



