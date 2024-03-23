#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 18.09.2020

import sys, os, glob, datetime, re
from selenium import webdriver #pip install selenium
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

class Browser:
    # method to register the client code
    def clientCode(self, url, outputPath, encoding='utf-8'):
        try:
            self.driver.get(url)
        except WebDriverException:
            print("Le code client du site : " + str(url) + " ne semble pas disponible")
        else:
            client_code = self.driver.page_source   #self.driver.find_element(By.XPATH,"//*").get_attribute("outerHTML")
            try:
                with open(outputPath, 'wb') as f:
                    f.write(client_code.encode(encoding))
            except OSError:
                radar = re.compile("http:__[A-z0-9.]*.onion")   # if the file name is to long for the OS, it will reduce the size of it
                name_finder = radar.findall(outputPath)
                new_name = name_finder[0]+"_shorted_clientCode.html"
                outputPath = "../../results/results_url_filter/"+ new_name
                with open(outputPath, 'wb') as f:
                    f.write(client_code.encode(encoding))
                print("Le nom du fichier était trop long pour le système et a donc été raccourcis\nNouveau nom : "+str(new_name))

    # method to register the client code
    def serverCode(self, outputPath, encoding='utf-8'):
        url = self.driver.current_url
        try:
            self.driver.get('view-source:'+url)
        except WebDriverException:
            print("le code serveur de l'url : " + str(url) + " n'est pas disponible")
        else:
            server_code = self.driver.find_element(By.XPATH,"//*").text
            self.driver.back()
            try:
                with open(outputPath, 'wb') as f:
                    f.write(server_code.encode(encoding))
            except OSError:
                radar = re.compile("http:__[A-z0-9.]*.onion")
                name_finder = radar.findall(outputPath)
                new_name = name_finder[0]+"_shorted_serverCode.html"
                outputPath = "../../results/results_url_filter/"+ new_name
                with open(outputPath, 'wb') as f:
                    f.write(server_code.encode(encoding))
    
    # method for the documentation
    def browsing_info(self, url, tor=False):
        if tor: proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'} #port 9050 si Tor est configuré comme un service
        else: proxies = {"http": None, "https": None}

        dateRequest = datetime.datetime.now().astimezone().isoformat() #date de la requête avec fuseau local
        documentation = {

            'date': dateRequest,
            'url_requested': url,
            'url_responsed': self.driver.current_url,
            'proxies': proxies,
        }
        return {'info': documentation}

    def __del__(self):
        try: self.driver.quit()
        except: None


class Firefox(Browser):
    def __init__(self, tor=False, headless=False, useragent=False):
        
        #Chemin vers le webdriver téléchargé - A changer si nécessaire
        if sys.platform == 'win32': driverFile = os.getcwd() + r'\webdrivers\geckodriver.exe' #Windows
        if sys.platform == 'darwin': driverFile = os.getcwd() + r'/webdrivers/geckodriver' #OSX
        
        #Configuration du webdriver
        options=Options()
        profile_path = glob.glob("/home/osint/.mozilla/firefox/*.default-esr")[0]
        options.set_preference('profile', profile_path)
        if headless: options.add_argument('--headless') #masque la fenêtre, False pour l'afficher
        options.set_preference("dom.push.enabled", False) #bloque les popup de notifications
        if useragent: options.set_preference("general.useragent.override", useragent)
        if tor:
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.socks', '127.0.0.1')
            options.set_preference('network.proxy.socks_port', 9150)
            options.set_preference('network.proxy.socks_version', 5)
            options.set_preference('network.proxy.socks_remote_dns', True)
        
        #Instanciation du webdriver
        self.driver = webdriver.Firefox(options=options)


