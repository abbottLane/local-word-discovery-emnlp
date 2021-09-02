from typing import List
import panphon.distance
import sys
import re
import getopt, sys
import ast
import os


FT = panphon.FeatureTable()
DST = panphon.distance.Distance()
GRAPHEME_PATTERN = re.compile('bb|kk|ng|dd|rdd|rd|rn|rl|rr|djdj|dj|nj|rr|b|m|k|g|d|n|l|r|y|h|d|a|e|i|o|u|.') # Defines the graphems of Kunwinjku orthography
ORTH2IPA = {
    "bb":"b",
    "ng":"ŋ",
    "dd":"t",
    "rdd":"ʈ",
    "rd":"ʈ",
    "rn":"ɳ",
    "rl":"ɭ",
    "rr":"r",
    "djdj":"ɟ",
    "dj":"ɟ",
    "nj":"ɲ",
    "b":"b",
    "m":"m",
    "k":"k",
    "g":"k",
    "d":"t",
    "n":"n",
    "l":"l",
    "r":"ɹ",
    "y":"j",
    "h":"ʔ",
    "d":"t",
    "a":"ɔ",
    "e":"ɛ",
    "i":"ɪ",
    "o":"ɔ",
    "u":"u"
}

def main():
    vocab_file = "evaluation/vocabs/sg_vocab.20.txt"
    tokens = load_tokens(vocab_file)
    
    phone_streams_dir = "evaluation/allo_transcriptions_sg/"
    phone_streams = load_dir_lines(phone_streams_dir)

    for s in phone_streams:
        top_result = align(tokens, s)
        print(top_result)

def load_dir_lines(in_dir):
    lines = []
    for i, filepath in enumerate(os.listdir(in_dir)):
        with open(os.path.join(in_dir,filepath), "r") as g:
            line = g.readline()
            lines.append(line.rstrip())
    return lines

def load_tokens(filepath):
    lines = []
    with open(filepath, "r") as f:
        lines = [x.split("\t")[0] for x in f.readlines()]
    return lines

def align(tokens, phones):
    top_positions = []
    print(phones)
    standardized_phones = standardize_phones(phones)
    for tok in tokens:
        graphemes = re.findall(GRAPHEME_PATTERN, tok)
        ipa = transform(graphemes)

        distance_and_position = []
        # slide ipa str accross phone sequence and pick the likely hits
        for position, ch in enumerate(standardized_phones):
            # tok_ft = FT.word_fts(ipa)
            # ref_ft = FT.word_fts(standardize_phones[position:len(ipa)])
            sub_seq = standardized_phones[position:position+len(ipa)]
            distance = DST.feature_edit_distance(ipa, sub_seq)
            distance_and_position.append(
                {
                    "distance": distance/len(ipa),
                    "start": position,
                    "stop": position + len(ipa) - 1
                }
            )
        minimum_full_length_match = {"token": tok, "alignment": min(distance_and_position, key=lambda x: x['distance'])}
        top_positions.append(minimum_full_length_match)

    return top_positions


def transform(graphemes: List[str]) -> str:
    new_str = ""
    for grapheme in graphemes:
        if grapheme in ORTH2IPA:
            new_str += ORTH2IPA[grapheme]
        else:
            new_str += grapheme
    return new_str

def standardize_phones(phones : str):
    """We are given a string of phones, possibly space delineated, possibly not. Lets just clean up the string to standardized form

    Args:
        phones (str): a str representing a phone sequence
    """
    phones = re.sub(" +", "", phones)
    return phones

if __name__ == "__main__":
    main()