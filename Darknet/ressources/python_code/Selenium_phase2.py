#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020
# updated: 01.09.2023

import time, json, sys, os, subprocess
from webdriver_phase2 import Firefox
from documentation_phase2 import Documentation # fichier documentation.py qui se trouve dans le dossier ressources

# Assignation du repertoire de travail
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

def saveData(browser, url, tor, filename_prefix="../../results/results_url_filter/"):  # la methode qui enregistre le code client, serveur et la docu
    crawl_info = browser.browsing_info(url, tor)
    browser.clientCode(url, filename_prefix+"client_codes/"+str(url.replace("/", "_"))+'_clientCode.html')
    browser.serverCode(filename_prefix+"server_codes/"+str(url.replace("/", "_"))+'_serverCode.html')   # les noms de fichier sont les urls de chaques pages
    return crawl_info


