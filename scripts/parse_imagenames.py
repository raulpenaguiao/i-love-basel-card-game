def remove_underscored_content(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open("new"+file_path, 'w') as file:
        for line in lines:
            if not '.jpg' in line:
                new_line = line
            else:
                last_underscore_index = line.rfind('_')
                last_string = line.rfind('.jpg')
                new_line = line[:last_underscore_index] + line[last_string:]
            file.write(new_line)

# Example usage
remove_underscored_content('card_info.json')