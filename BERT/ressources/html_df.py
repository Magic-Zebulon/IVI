import os
import string
from html import unescape

import pandas as pd
import lxml.html
from sentence_transformers.models.tokenizer import ENGLISH_STOP_WORDS


def preprocess_text(text):
    # Remove HTML entities
    text = unescape(text)

    # Remove characters related to HTML structure
    text = ''.join([char for char in text if char not in ['<', '>', '/', '=', '"', "'"]])

    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word.lower() not in ENGLISH_STOP_WORDS])
    # Remove numbers
    text = ''.join([char for char in text if not char.isdigit()])
    return str(text)

def html_dict(path):
    text_content = lxml.html.parse(path).getroot().text_content()
    text_content = preprocess_text(text_content)
    id = path.split('/')[-1]
    liste_id_text = [id, text_content] # liste contenant l'id et le texte clean
    return liste_id_text


def from_list_to_df(liste_path):
    df = pd.DataFrame()
    n = 0
    for html in liste_path:  # new, top, hot, etc. limit:réglé à None collecte un maximum de résultats possible
        liste_url_content = html_dict(html)
        n+=1
        row = {
            'id': n,
            'url': liste_url_content[0],  # Collecte de l'id
            'text': liste_url_content[1],  # contenu texte clean du html
        }
        # Ajout des résultats au dataframe
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    return df


if __name__ == '__main__':
    liste_path = [] # liste des chemins vers les fichiers html
    for i in range(2):
        if i == 0:
            path_directory = '/results_phase2/ClearWeb/results/code_client'
        else:
            path_directory = '/results_phase2/code_client_serveur/client_code'


        for filename in os.listdir(path_directory): # parcours du dossier
            if filename != '.DS_Store':
                liste_path.append(path_directory + '/' + filename)
        df = from_list_to_df(liste_path)
    print(f"df  generated: {df}")
