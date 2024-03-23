import time, json, sys, os, subprocess
from webdriver import Firefox
from documentation import Documentation 

# Assignation du repertoire de travail
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
       
# this method is used to call functions that will register client/server codes, as well as to record information for documentation purposes
def saveData(browser, url, input_Cc, input_Cs, filename_prefix= "../../results/results_url_finder/client_server_codes/"):
    crawl_info = browser.browsing_info(url, tor=False)
    browser.clientCode(url, filename_prefix+ "CodeClient_" +input_Cc)
    browser.serverCode(filename_prefix+ "CodeServeur_" +input_Cs)
    return crawl_info

   