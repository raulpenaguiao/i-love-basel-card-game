import re

def remove_quotes_from_file(input_file, output_file):
    counter = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            pattern = re.compile(r'card\d{3}\.jpg')
            line = pattern.sub('card' + f'{counter:03d}' + '.jpg', line)
            counter += 1
            outfile.write(line.replace('"', ''))

if __name__ == "__main__":
    input_file = 'places_basel_cards.csv'  # Replace with your input file path
    output_file = 'places_basel_cards_1.csv'  # Replace with your output file path
    remove_quotes_from_file(input_file, output_file)