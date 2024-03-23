#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 18.09.2020

import sys, os, datetime
from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By

class Browser:
    def clientCode(self, url, outputPath, encoding='utf-8'):
        """Enregistre le code client"""
        self.driver.get(url)
        client_code = self.driver.page_source    #self.driver.find_element(By.XPATH,"//*").get_attribute("outerHTML")
        with open(outputPath, 'wb') as f:
            f.write(client_code.encode(encoding))

    def serverCode(self, outputPath, encoding='utf-8'):
        url = self.driver.current_url
        self.driver.get('view-source:'+url)
        server_code = self.driver.find_element(By.XPATH,"//*").text
        self.driver.back()
        with open(outputPath, 'wb') as f:
            f.write(server_code.encode(encoding))
    
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

# Nombreux paramètres possibles :https://developer.mozilla.org/en-US/docs/Web/WebDriver/Commands et https://firefox-source-docs.mozilla.org/dom/push/index.html 
class Firefox(Browser):
    def __init__(self, tor=False, headless=False, useragent=False):

        #Configuration du webdriver
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')  # enlever le commentaire pour masquer la fenêtre

        #options.set_preference("dom.push.enabled", False) #bloque les popup de notifications
        #options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36") #définit un useragent
        #options.set_preference('permissions.default.image', 2) #desactive les images
        #options.set_preference('image.animation_mode', 'none') #desactive les animations
        if headless: options.add_argument('--headless') #masque la fenêtre, False pour l'afficher
        options.set_preference("dom.push.enabled", False) #bloque les popup de notifications
        if useragent: options.set_preference("general.useragent.override", useragent)
        if tor:
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.socks", "127.0.0.1")
            options.set_preference("network.proxy.socks_port", 9150) #Port de Tor
            options.set_preference("network.proxy.socks_version", 5)
            options.set_preference("network.proxy.socks_remote_dns", True)

        #Instanciation du webdriver
        self.driver = webdriver.Firefox(options=options)
