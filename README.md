# IVI : Organ trafficking extraction and analysis

If you want to have an easy access to the code you can ask for access to the private GitHub repository by email with your GitHub account name.

## Features

### Collects:  
- Website url related to organ trafficking from search engines onionland.onion and ahmia.fi using keyword organ
- Scrapes the client and server codes from darknet and clearweb websites

### Analysis:
- Extraction of the text content of the client codes from root and from body
- Extraction of html class names of the client codes from the selected clearweb and darknet websites
#### Bertopic analysis of :
  - Text content of Client code from root
  - Text content of Client code from body
  - Html class names from the client code


## Requirements

Python 3.9 to latest version is required.

### Dependencies

Dependencies for your python environment are listed in `requirements.txt`. Install them using the below command. Ensure 
the `py` part is correct for your environment, eg `py`, `python`, or `python3`, etc. 

`py -m pip install -r requirements.txt`  
or  
 `pip3 install -r requirements.txt`

**Important : Bertopic modding is required to run the code.**

### How to mod Bertopic :
1. Find where the project interpreter is installed
2. Go to "site-packages/bertopic/plotting"
3. Look for the file "_documents.py", rename it to "_documents_original.py"
4. Copy the file "_documents.py" from the folder "Bertopic_mod" to the folder "plotting"

# How to run the code:

#### 1. Clone the repository

#### 2. Install the dependencies

#### 3. From Darknet folder run the following command:

   1. python3 lxml_extraction.py : Choose option 1 to scrape from ahmia.fi, option 2 to scrape from onionland.onion and option 3 to scrape from both the search engines
   2. Results from the scraping will be stored in the folder named "results"
   3. Scraping documentation will be stored in the folder named "documentation" found in the folders results_url_finder and results_url_filter

#### 4. From Clearweb folder run the following command:

   1. python3 clearWebscript.py : The name for the documentation file will be asked
   2. Results from the scraping will be stored in the folder named "results/code_client_serveur"
   3. Documentation will be stored in the folder named "docu_phase1"

#### 5.  From html_extraction folder run the following command:

   1. Run all the python files in the folder ressources
   2. Results will be in the dictionnaire folders
   3. Note: The extraction is done from the html_files folder

#### 6.  From the BERT folder run the following command:

   1. The ressources are jupyter notebooks : 
      1. BERT_website_root.ipynb : Bertopic analysis of the text content of the client code from root
      2. BERT_website_body.ipynb : Bertopic analysis of the text content of the client code from body
      3. BERT_html_class.ipynb : Bertopic analysis of the html class names of the client code
   2. For each run of the notebook, the results will be stored in the folder named "results":
      3. Note: Every run of the notebook will overwrite the previous results if you do not change the name of the file in the notebook
   3. The code is directly linked to the results of the previous steps, so you need to run the previous steps before running the BERTopic analysis

