import os
import json
from xml.etree import ElementTree
import re
import csv


def convert_to_fsw(layout_txt_content):
    # Fixing img tags to be self-closing for XML parsing
    layout_txt_content = re.sub(r'<img([^>]+)/?>', r'<img\1/>', layout_txt_content)
    layout_txt_content = layout_txt_content.replace('&size=.7', '')

    root = ElementTree.fromstring(layout_txt_content)
    max_x, max_y = int(root.get('max_x')), int(root.get('max_y'))
    fsw = f'M{max_x + 500}x{max_y + 500}'

    for sym in root.findall('sym'):
        key = sym.find('img').get('src').split('key=')[1]
        left, top = int(sym.get('left')), int(sym.get('top'))
        fsw += f'S{key}{left + 500}x{top + 500}'
    return fsw


def process_directory(directory, lexicon):
    results = []
    for dir_name, _, _ in os.walk(directory):
        layout_path = os.path.join(dir_name, 'layout.txt')
        if os.path.isfile(layout_path):
            with open(layout_path, 'r') as file:
                content = file.read()
                fsw = convert_to_fsw(content)
                name = os.path.basename(dir_name)
                if name not in lexicon:
                    print(f"Missing {name}")
                    continue
                results.append({
                    # need to pad Nr to 5 digits
                    "file": f"illustrations/{lexicon[name]['Nr'].zfill(5)}.png",
                    "fsw": fsw,
                    "meta": lexicon[name]
                })

    with open('writing.json', 'w') as json_file:
        json.dump(results, json_file)


def parse_lexicon_tsv():
    with open('lexicon.tsv', 'r', encoding='mac_latin2') as file:
        dict_reader = csv.DictReader(file, delimiter='\t')
        # Convert the reader to a list to return it
        return {row['Glosse']: row for row in dict_reader}


if __name__ == "__main__":
    lexicon = parse_lexicon_tsv()
    print(len(list(lexicon.keys())))
    process_directory('SW_signs_glosses', lexicon)
