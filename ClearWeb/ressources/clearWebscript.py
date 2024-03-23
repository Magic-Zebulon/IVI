import selenium
import datetime
from selenium import webdriver
import time, json, sys, os, subprocess
from webdriver import Firefox
import documentation

# Assignation du repertoire de travail
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

def saveData(browser, url, tor, input_C, filename_prefix):
    crawl_info = browser.browsing_info(url, tor)
    browser.clientCode(url, filename_prefix+ "/CodeClient_" +input_C+'.html')
    browser.serverCode(filename_prefix+ "/CodeServeur_" +input_C+'.html')
    return crawl_info

def Info_Extractor(browser, request):
    doc = documentation.Documentation(driver=browser.driver)
    doc.info = request["info"]
    #    doc.info = crawl_info['info']
    with open("../docu_phase1/"+input("entrez 1 nom pour nommer le fichier de documentation : "), "wb") as f:
        f.write(str(doc).encode("utf-8"))

driver = webdriver.Firefox()

# ~~~~~~~~~~~~ Corps du programme ~~~~~~~~~~~~~ #
if __name__ == '__main__':
    # ~~~~~~~~~~~~~~~ Début Selenium ~~~~~~~~~~~~~~~ #
    tor = True  # Paramétrage activation/désactivation de Tor
    browser = Firefox(tor, headless=False)  # ou Chrome(...)
    # Vous pouvez compléter l'objet doc avec les urls parcourues et les manipulations effectuées!
    list_url = ["https://organcity.com/", "https://groodcity.com/", "https://activescienceparts.com/","https://organ-city.com/"]
    for url in list_url:
        driver.get(url)
        input_C = input("Entrez un nom de fichier pour le code : ")
        #browser.driver.get(url)
        scrapy = saveData(browser, url, tor,input_C, filename_prefix='../results/code_client_serveur')
        Info_Extractor(browser, scrapy)

    driver.close()

