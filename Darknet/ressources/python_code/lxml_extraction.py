import lxml.html as lx
import to_SQL
import sqlite3
import Selenium
import datetime
from webdriver import Firefox
import documentation
import Filtre_phase2
import sql_phase2


# This method manages the user's choice by directing them to the right method depending on which site they want to scrape.
def Client_Extractor():
    choix = input("Quels sites voulez-vous 'Scraper' ?\n1) Pour scraper Ahmia.fi, tapez 1\n2) Pour scraper OnionLand.onion, tapez 2\n3) pour Scraper les 2 sites, tapez 3\nvotre réponse : ")
    if choix == "1" :
        choix="https://ahmia.fi/search/?q=organs&d=7"
    elif choix == "2" :
        choix = "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q=organs&page="
    elif choix == "3":
       choix = "liste"

    if choix == "https://ahmia.fi/search/?q=organs&d=7" :
        ahmia_extractor(choix)
    elif choix == "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q=organs&page=" :
        onion_extractor(choix)
    elif choix == "liste":
        choix = ["http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search?q=organs&page=", "https://ahmia.fi/search/?q=organs&d=7"]
        for url in choix:
            if url == "https://ahmia.fi/search/?q=organs&d=7":
                ahmia_extractor(url)
            else:
                onion_extractor(url)

# this method writes the "documentation" file for each scrapper site.
def Info_Extractor(navi, request, input_Cc):
    doc = documentation.Documentation(driver=navi.driver)
    doc.info = request["info"]
    with open("../../results/results_url_finder/documentation/"+input_Cc+str(datetime.datetime.now()), "wb") as f:
        f.write(str(doc).encode("utf-8"))

def ahmia_extractor(choix):
    input_Cc = "ahmia_"+str(datetime.datetime.now())
    input_Cs = "ahmia_"+str(datetime.datetime.now())
    navigateur = Firefox()
    scraper = Selenium.saveData(navigateur, choix, input_Cc, input_Cs)
    Info_Extractor(navigateur, scraper, input_Cc)
    html = lx.parse("../../results/results_url_finder/client_server_codes/"+"CodeClient_"+input_Cc).getroot()
    to_SQL.addDataSqliteDatabase(connexion, Result_Extractor(html, choix, input_Cc, input_Cs))
# These two functions will call the method to register client and server codes. Then parse the html client code, and 
# then call the method to add the result in the database
def onion_extractor(choix):
    navigateur = Firefox(tor=True)
    for i in range(2):
        input_Cc = "OnionLand_"+str(datetime.datetime.now())
        input_Cs = "OnionLand_"+str(datetime.datetime.now())
        scraper = Selenium.saveData(navigateur, choix+str(int(i)+1), input_Cc=input_Cc, input_Cs=input_Cs)
        Info_Extractor(navigateur, scraper, input_Cc)
        html = lx.parse("../../results/results_url_finder/client_server_codes/"+"CodeClient_"+input_Cc).getroot()
        to_SQL.addDataSqliteDatabase(connexion, Result_Extractor(html, choix, input_Cc, input_Cs))

# This method extracts urls, titles, description and, if possible, the date of publication of the urls. 
# Return a list [] with, in addition, the datetime.now() and the client and server codes.
def Result_Extractor(html, url, Cc, Cs):
    check = ".onion"
    liste_finale = []
    index = 0
    compte = 1
    if check in url:
        titles = html.find_class("title")
        descriptions = html.find_class("desc")
        links1 = html.xpath("link")
        links2 = html.xpath("/html/body/div[2]/div[4]/div/div[1]/div/div/div/div/div[2]")  # Anti-scrapping method from the webpage OnionLand. Many tags are empty. 
        if links2 == None:                                                                 # we must select those that contain a value.
            links = links1
        else:
            links = links2
        while index <= int(len(titles)-1):
            liste_finale.append((links[index].text_content(), titles[index].text_content(), descriptions[index].text_content(), "Void",
                                  datetime.datetime.now(), Cc, Cs))
            index=index+1
            compte=compte+1 
    else:
        titles = html.xpath("//*[@id='ahmiaResultsPage']/ol/li/h4/a")       # extracting the infos from ahmia.fi
        descriptions = html.xpath("//*[@id='ahmiaResultsPage']/ol/li/p")
        links = html.xpath("//*[@id='ahmiaResultsPage']/ol/li/cite")
        publications = html.xpath("//*[@id='ahmiaResultsPage']/ol/li/span")
        while index <= int(len(titles)-1):
            liste_finale.append((links[index].text_content(), titles[index].text_content(), descriptions[index].text_content(), publications[index].text_content(), 
                                 datetime.datetime.now(), Cc, Cs))
            index=index+1
            compte=compte+1
    return liste_finale
   

if __name__ == "__main__" :
    connexion = sqlite3.connect('../../results/darknet_url.db')     # connexion to the database 'darknet_url' 
    to_SQL.createSqliteTable(connexion)                             # first we need to create the table 'url_finder'
    Client_Extractor()
    to_SQL.Mr_propre(connexion)                                     # this method is made to clean the database.
    sql_phase2.createSqliteTable(connexion)
    connexion.close()
    Filtre_phase2.Starting_block()

    print("\nLEEEEEEEEEEROOOOOOOOOOOOOOY JEEEEEEEEENNNNNNKIIIIIIIIINNNNNSSSSSS\n")