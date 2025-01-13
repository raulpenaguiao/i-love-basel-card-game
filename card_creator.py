import subprocess
import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def NewCard(card, card_front_template):
    new_card = card_front_template.replace("##Image##", "resources/imgs/cards/" + card["PictureName"])
    new_card = new_card.replace("##Title##", card["Name"])
    new_card = new_card.replace("##Type##", card["Type"])
    new_card = new_card.replace("##Description##", card["Description"])
    new_card = new_card.replace("##SmallDescription##", card["SmallDescription"])
    new_card = new_card.replace("##Coordinates##", str(round(card["XCoordinates"], 5)) + "$^{\circ}$N " + str(round(card["YCoordinates"], 5)) + "$^{\circ}$E")
    return new_card

def create_tex_file_cards(data, output_path, card_front_template_path, card_back_template_path):
    #Get data from JSON file
    data_json = read_json(data)
    data_json_cards = data_json["cards"]
    
    #Get the card template text
    card_front_template = ""
    with open(card_front_template_path, 'r') as file:
        card_front_template = file.read()

        
    #Get the card template text
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
    #make sure we are printing a multiple of 6 cards
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
    content = ""
    for i in range(number_pages):
        content += "\hspace{-3mm}\n"
        for j in range(3):
            content += new_cards_front[i*6 + j] + middle_string
        content += "\n\n\\vspace{5mm}\n\n\hspace{-2.5mm}\n"
        for j in range(3,6):
            content += new_cards_front[i*6 + j] + middle_string
        content += "\n\n\\vspace{5mm}\n\n\hspace{-2.5mm}\n"
        for j in range(2, -1, -1):
            content += new_cards_back[i*6 + j] + middle_string
        content += "\n\n\\vspace{5mm}\n\n\hspace{-2.5mm}\n"
        for j in range(5, 2, -1):
            content += new_cards_back[i*6 + j] + middle_string
        content += "\n\n\\vspace{5mm}\n\n"
    #emove last middle string
    content = content[:-len(middle_string)]

    with open(output_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    json_file_path = 'card_info.json'  # Change this to your JSON file path
    tex_file_path = 'templated_cards.tex'
    card_front_template_path = "card_front_template.tex"
    card_back_template_path = "card_back_template.tex"
    create_tex_file_cards(json_file_path, tex_file_path, card_front_template_path, card_back_template_path)
    subprocess.run(['pdflatex', 'cards.tex'])