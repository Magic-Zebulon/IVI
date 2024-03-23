from ast import main
import re, os 
from webdriver_phase2 import Firefox
import Selenium_phase2
import documentation_phase2
import sql_phase2
import lxml.html as lx
import sqlite3 as sql

# takes the information from the 'url_finder' table and transforms it into a list for working with
def Starting_block():
    liste_url = sqlite_to_list_url()
    liste_title = sqlite_to_list_title()
    liste_description = sqlite_to_list_description()
    index = 0
    compteur = 1
    for url in liste_url:
        print("Début du scrapping du site internet : " + str(url) + "\nSite n° : "+str(compteur))
        save_html(url)
        try:     # save client code, server code and documentation.
            code_source = lx.parse("../../results/results_url_filter/client_codes/"+str(url.replace("/", "_"))+'_clientCode.html').getroot()
        except OSError: # this part of the code handles cases where the web page or server is unavailable
            print("""\nerreur à lire la page n° : "+str(compteur)+"\nLe code client n'a pas été extrait, peut-être que le page n'éxiste plus.
                  Ou alors il s'agit d'une erreur 404 ou 502.\n-------------------------------------------------------------------------------------------------------------------------------""")
            index = index+1
            compteur=compteur+1
        else:                                                           
            filtre_regexp(code_source, url, liste_title[index], liste_description[index])
            print("\nLe site n° : "+str(compteur) + " a été extrait" +"\n"+"-------------------------------------------------------------------------------------------------------------------------------") 
            index=index+1 
            compteur = compteur+1
    print("\n Tous les sites ont été scrappés !! \n") 
    html_keyword()
      
# this method uses the regexp module to detect a list of words in the scrapped page body. 
def filtre_regexp(source_code, url, title, description):
    radar = re.compile("organs?|kidneys?|hearts?|lungs?|livers?|meat|flesh|human body|human bodies|surgeons?|surgery", re.IGNORECASE) 
    contenu = source_code.cssselect("body") # we create a list of words that should appear in the body of web pages selling organs.
    detector= radar.findall(contenu[0].text_content()) 
    if detector:
        print("la page web : "+str(title)+ " contient des mots clés.\nURL : "+str(url))
        sql_phase2.add_db(url, title, description, statut = ", ".join(detector), valeur=1) # if the webpage contains keyword, it will be  
    else:                                                                                  # add in the database with the value 1. Else 0
        print("la page web : "+str(title)+ " ne contient aucun des mots clés.\nURL : "+str(url))
        sql_phase2.add_db(url, title, description, statut = "Ne contient pas de mots clés", valeur=0)
        
def save_html(webpage):                 # this method saves client code, server code and documentation. 
    navigateur = Firefox(tor=True)      # Note that the 'save_Data' method takes care of this.
    scrapy = Selenium_phase2.saveData(navigateur, webpage, tor=True)
    Info_extractor(navigateur, scrapy, webpage)

# This method copies html client codes that have keywords in their body. These copies are saved in a new folder. 
# This is important for the analysis part.
def html_keyword():
    conn = sql.connect('../../results/darknet_url.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM url_filter WHERE valeur = 1")
    rows = cursor.fetchall()
    source_folder = "../../results/results_url_filter/client_codes/"
    destination_folder = "../../results/results_url_filter/html_keyword/"
    for row in rows:
        url = row[0]
        url = url.replace("_", "/")
        url = url.replace("/", "_")
        file_name = os.path.basename(url) + "_clientCode.html"
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        temoin = 1
        try:
            with open(source_path, 'rb') as source_file, open(destination_path, 'wb') as destination_file:
                destination_file.write(source_file.read())
                temoin=temoin+1
        except FileNotFoundError:
            print(f"Le fichier {file_name} n'a pas été trouvé dans le dossier source.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la copie du fichier {file_name}: {e}")
    conn.close()
    print("Un total de "+str(temoin)+" fichiers ont été copiés avec succès")

# this method transforms the 'url' column in the database into a list so that you can work on it. Returns a list
def sqlite_to_list_url():   
    liste = []
    connector = sql.connect("../../results/darknet_url.db") # connexion a la database
    cursor = connector.cursor()
    cursor.execute("SELECT URL FROM url_finder")
    res = cursor.fetchall()   
    for raw in res:
        liste.append(raw[0])
    cursor.close
    return liste  

# this method transforms the 'title' column in the database into a list so that you can work on it. Returns a list    
def sqlite_to_list_title():   
    liste = []
    connector = sql.connect("../../results/darknet_url.db")
    cursor = connector.cursor()
    cursor.execute("SELECT title FROM url_finder")
    res = cursor.fetchall()
    for raw in res:
        liste.append(raw[0])
    cursor.close()
    return liste

# this method transforms the 'description' column in the database into a list so that you can work on it. Returns a list
def sqlite_to_list_description():
    liste = []
    connector = sql.connect("../../results/darknet_url.db")
    cursor = connector.cursor()
    cursor.execute("SELECT description FROM url_finder")
    res = cursor.fetchall()
    for raw in res:
        liste.append(raw[0])
    cursor.close()
    return liste

# for the documentation
def Info_extractor(navi, request, webpage):     
    doc = documentation_phase2.Documentation(driver=navi.driver)
    doc.info = request["info"]
    with open("../../results/results_url_filter/documentation/"+str(webpage.replace("/","__")), "wb") as f:
        f.write(str(doc).encode("utf-8"))



