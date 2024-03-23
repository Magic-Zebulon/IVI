
import lxml.html
import re
import json

Html = lxml.html.parse("/Users/admin/Documents/MA-1.2/ACO/TPs/IVI/4_http___scaa6fzk2n2rj5gxtv3p5nmbfhvu6wscj4vysw7hz3pycawsekdimhyd.onion_product=buy-potassium-cyanide-online_clientCode.html").getroot()

texte = str(lxml.html.tostring(Html), 'utf-8')


class_results = re.findall('class\=\"(.*?)\"', texte)
split_class_results = [re.split(r'\s', class_name) for class_name in class_results]
flat_class_results = [item for sublist in split_class_results for item in sublist]

id_results = re.findall('id\=\"(.*?)\"', texte)
split_id_results = [re.split(r'\s', id_name) for id_name in id_results]
flat_id_results = [item for sublist in split_id_results for item in sublist]

unique_class_results = []
seen_classes = set()
for class_name in flat_class_results:
    if class_name not in seen_classes:
        seen_classes.add(class_name)
        unique_class_results.append(class_name)

unique_id_results = []
seen_ids = set()
for id_name in id_results:
    if id_name not in seen_ids:
        seen_ids.add(id_name)
        unique_id_results.append(id_name)


# print("Unique Class Attributes:", unique_class_results)
# print("Unique ID Attributes:", unique_id_results)


attribute_dict_4_Darkweb = {'class': unique_class_results, 'id': unique_id_results}

with open('../dictionnaire/attribute_dict_4_Darkweb.json', 'w') as json_file:
    json.dump(attribute_dict_4_Darkweb, json_file)

print("Attributes Dictionary:")
print(attribute_dict_4_Darkweb)
print("Attributes Dictionary has been saved to attribute_dict_4_Darkweb.json")

# with open('attribute_dict_Organcity.json', 'r') as json_file:
#     loaded_dict = json.load(json_file)

# print("Loaded Attributes Dictionary:")
# print(loaded_dict)