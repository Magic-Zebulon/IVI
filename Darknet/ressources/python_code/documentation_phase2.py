#!/usr/bin/env python
# coding=utf-8
# author: T. Pineau
# creation: 19.09.2020

import os, platform, json, re, subprocess
from pipreqs import pipreqs # pip install pipreqs
import requests # pip install requests requests[socks] pysocks
from selenium.webdriver.common.by import By

class Documentation():
    def __init__(self, tor=False, info={}, driver=False):
        self.path = os.path.dirname(os.path.realpath(__file__)) #le chemin du dossier où est exécuté le fichier
        self.info = info
        self.program = {
            'software': "Python",
            'software_version': platform.python_version(),
            'modules': pipreqs.get_all_imports(self.path, encoding='utf-8') # pipreqs.get_imports_info() permet d'avoir la version des module, présence de bug
        }
        info = re.sub('\s{2,}','',subprocess.check_output("lscpu").strip().decode())
        elem = ['Architecture:(.*)', '(family:.*)', '(Model:.*)', '(Stepping:.*)', 'Vendor ID:(.*)']
        processor_info = ' '.join(re.search(pattern, info).group(1) for pattern in elem if re.search(pattern, info))
        self.system = {
            'os_name': platform.system(),
            'computer_name': platform.node(),
            'os_release': platform.release(),
            'os_version': platform.version(),
            'processor': processor_info
        }
        self.ip = ''
        if driver:
            try:
                driver.get('http://httpbin.org/ip')
                content = driver.find_element(By.XPATH,"//body").text
                self.ip = json.loads(content)['origin']
            except: print('Documentation - erreur à retrouvé l\'adresse IP publique.')
        else:
            if tor: proxies = {'http': 'socks5h://127.0.0.1:9150', 'https': 'socks5h://127.0.0.1:9150'} #port 9050 si Tor est configuré comme un service
            else: proxies = {"http": None, "https": None}
            try: self.ip = requests.get('http://httpbin.org/ip', proxies=proxies).json()['origin'] #utilisation du service ipinfo.io
            except: print('Documentation - erreur à retrouvé l\'adresse IP publique.')


    def toJSON(self):
        """Retourne l'objet dans le format JSON"""
        return {
            'ip': self.ip,
            'programm': self.program,
            'system': self.system,
            'info': self.info
        }

    def __str__(self):
        """Pour afficher l'objet avec la fonction print(objet)"""
        return json.dumps(self.toJSON(), indent=4)
