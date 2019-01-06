import re
import pandas as pd

filename = "anki.txt"
section_split = r"\\section"
card_split = r"\\card"
double_dolars = "\$\$(.*?)\$\$"
single_dolars = "\$([^\[\$\]][^\$]*?[^\/\[\$])\$"

def make_anki(string):
    double_dolars_str = re.sub(double_dolars, r"[$$]\1[/$$]", string)
    single_dolars_str = re.sub(single_dolars, r"[$]\1[/$]", double_dolars_str)
    return single_dolars_str

def prepare_card(raw_card):
    raw_front, raw_back = raw_card.split("\n", 1)
    front = raw_front[1:-1]
    raw_back = raw_back.strip("\t")
    back = re.sub(r"[\n]*$", "",raw_back.strip(" ")).rstrip("\n")
    back = back.replace("\\\n","<br>")
    return [make_anki(front), make_anki(back).replace("\n","<br>")]

def main():
    file = open(filename, "r")
    text = file.read()

    sections = re.split(section_split,text)[1:]
    sections_cards = [re.split(card_split,section)[1:] for section in sections]
    cards = list(sum(sections_cards, []))

    anki_cards = [prepare_card(card) for card in cards]
    df = pd.DataFrame(anki_cards)
    df.to_csv("anki.csv", header=None, index=None)

if __name__== "__main__":
  main()
