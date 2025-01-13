import subprocess
import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_tex_file(data, output_path, card_template_path):
    #Get data from JSON file
    data_json = read_json(data)
    data_json_cards = data_json["cards"]
    
    #Get the card template text
    card_template = ""
    with open(card_template_path, 'r') as file:
        card_template = file.read()
    
    #Create a new card for each card in the JSON file
    new_cards = []
    for card in data_json_cards:
        new_card = card_template.replace("##Image##", "resources/imgs/" + card["PictureName"])
        new_card = new_card.replace("##Title##", card["Name"])
        new_card = new_card.replace("##Type##", card["Type"])
        new_card = new_card.replace("##Description##", card["Description"])
        new_card = new_card.replace("##Image##", str(round(card["XCoordinates"], 5)) + " - " + str(round(card["YCoordinates"], 5)))
        new_cards.append(new_card)
    
    #Start producing the content of the .tex file and output
    content = "\n\n\hspace{5mm}\n\n".join(new_cards)
    with open(output_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    json_file_path = 'card_info.json'  # Change this to your JSON file path
    tex_file_path = 'templated_cards.tex'
    card_template_path = "card_template.tex"
    create_tex_file(json_file_path, tex_file_path, card_template_path)
    subprocess.run(['pdflatex', 'cards.tex'])