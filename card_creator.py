import subprocess
import json
import pandas as pd


ROUNDING_DIGITS = 4

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def NewCard(card, card_front_template):
    if card["FrontPictureName"] == "":
        card["BackPictureName"] = "nia.jpg"
    if card["FrontPictureName"] == "":
        card["BackPictureName"] = "nia.jpg"
    new_card = card_front_template.replace("##FrontImage##", "resources/imgs/cards/" + card["FrontPictureName"])
    new_card = new_card.replace("##BackImage##", "resources/imgs/cards/" + card["BackPictureName"])
    new_card = new_card.replace("##Title##", card["GermanName"])
    new_card = new_card.replace("##Type##", card["Category"])
    new_card = new_card.replace("##Description##", card["Description"])
    new_card = new_card.replace("##SmallDescription##", card["SmallDescription"])
    digit_format = '.' + str(ROUNDING_DIGITS)+'f'
    formatted_coordinates = format(card["NCoordinate"], digit_format) + "$^{\circ}$N " + format(card["ECoordinate"], digit_format) + "$^{\circ}$E"
    new_card = new_card.replace("##Coordinates##", formatted_coordinates)
    return new_card

def create_tex_file_cards(data, output_path, card_front_template_path, card_back_template_path):
    #Get data from JSON file
    data_json = read_json(data)
    data_json_cards = data_json["cards"]
    
    #Get the card template text
    card_front_template = ""
    with open(card_front_template_path, 'r') as file:
        card_front_template = file.read()
    card_back_template = ""
    with open(card_back_template_path, 'r') as file:
        card_back_template = file.read()
    
    #Create a new card for each card in the JSON file
    number_cards = len(data_json_cards)
    new_cards_front = []
    new_cards_back = []
    for card in data_json_cards:
        new_cards_front.append(NewCard(card, card_front_template))
        new_cards_back.append(NewCard(card, card_back_template))
    #make sure we are printing a multiple of cards_per_page cards
    cards_per_page = 6
    if number_cards%cards_per_page > 0:
        card = data_json_cards[0]
        for _ in range((cards_per_page-number_cards)%cards_per_page):
            new_cards_front.append(NewCard(card, card_front_template))
            new_cards_back.append(NewCard(card, card_back_template))
    number_cards = len(new_cards_back)
    number_pages = number_cards // 6
    


    #Start producing the content of the .tex file and output
    middle_string = "\n\hspace{1mm}\n"
    break_line_string = "\end{center}\n\n\\vspace{5mm}\n\n\\begin{center}\n"
    content = ""
    for i in range(number_pages):
        content += "\\begin{center}\n"
        for j in range(3):
            content += new_cards_front[i*6 + j] + middle_string
        content += break_line_string
        for j in range(3,6):
            content += new_cards_front[i*6 + j] + middle_string
        content += break_line_string
        for j in range(2, -1, -1):
            content += new_cards_back[i*6 + j] + middle_string
        content += break_line_string
        for j in range(5, 2, -1):
            content += new_cards_back[i*6 + j] + middle_string
        content += "\n\n\end{center}\n\n"
    #remove last middle string
    content = content[:-len(middle_string + "\n\n\end{center}\n\n")]  + "\n\n\end{center}\n\n"

    with open(output_path, 'w') as file:
        file.write(content)


def create_json_file(excel_file_paths, json_file_path):
    data_json = {}
    data_cards = pd.read_csv(excel_file_paths["cards"]).fillna('')
    data_json["cards"] = []
    for _, row in data_cards.iterrows():
        card = {}
        card["GermanName"] = row["GermanName"]
        card["EnglishName"] = row["EnglishName"]
        card["Neighbourhood"] = row["Neighbourhood"]
        card["GMapsLink"] = row["GMapsLink"]
        card["Category"] = row["Category"]
        card["Description"] = row["Description"]
        card["SmallDescription"] = row["SmallDescription"]
        card["NCoordinate"] = row["NCoordinate"]
        card["ECoordinate"] = row["ECoordinate"]
        card["FrontPictureName"] = row["FrontPictureName"]
        card["BackPictureName"] = row["BackPictureName"]
        data_json["cards"].append(card)
    
    data_json["neighbourhoods"] = []
    data_neighbourhoods = pd.read_csv(excel_file_paths["neighbourhoods"]).fillna('')
    for _, row in data_neighbourhoods.iterrows():
        neighbourhood = {}
        neighbourhood["GermanName"] = row["GermanName"]
        neighbourhood["EnglishName"] = row["EnglishName"]
        neighbourhood["PictureName"] = row["PictureName"]
        data_json["neighbourhoods"].append(neighbourhood)

    data_json["categories"] = []
    data_categories = pd.read_csv(excel_file_paths["categories"]).fillna('')
    for _, row in data_categories.iterrows():
        category = {}
        category["GermanName"] = row["GermanName"]
        category["EnglishName"] = row["EnglishName"]
        category["PictureName"] = row["PictureName"]
        data_json["categories"].append(category)

    with open(json_file_path, 'w') as file:
        json.dump(data_json, file)


if __name__ == "__main__":
    excel_file_paths = {  #Excel file paths
        "cards":'places_basel_cards.csv', 
        "neighbourhoods": 'places_basel_neighbourhoods.csv', 
        "categories":'places_basel_categories.csv'
    }
    json_file_path = 'card_info.json'  #JSON file path
    tex_file_path = 'templated_cards.tex'
    card_front_template_path = "card_front_template.tex"
    card_back_template_path = "card_back_template.tex"
    create_json_file(excel_file_paths, json_file_path)
    create_tex_file_cards(json_file_path, tex_file_path, card_front_template_path, card_back_template_path)
    subprocess.run(['pdflatex', 'cards.tex'])