import argparse
import re
import csv
from HFST_Model import HFSTModel

HFST_MODEL = HFSTModel("kunwok-acceptor.min.bin.hfst")

def main(input_file=None, known_vocab=None, evaluate=False):
    result_data = []
    known_tokens = load_known_vocab(known_vocab)
    if input_file:
        with open(input_file, "r") as f:
            print(input_file)
            lines = f.read().split("\n\n")
            for i, line in enumerate(lines):
                print("Processed " + str(i) + " speech docs out of " + str(len(lines)))
                sparse_line = line.split('\n')[0]
                gold_line = line.split('\n')[1]
                
                # # test: remove line below later
                # line = "ng a l e k ɐ bolk n ɐ n"
                results = HFST_MODEL.apply_down(" " + sparse_line.rstrip() + " ") # pad with blank space on both side so we catch beginning words                
                results = [re.sub("-", "", x) for x in results] # Strip offsets
                results = ["".join(x.split()) for x in results if has_overlap(x.split(), known_tokens)] # filter out suggestions not grounded in known lexeme
                if not evaluate:
                    print(line.rstrip() + "\n" + "\n".join(results) + "\n")
                result_data.append({
                    "suggestions": results,
                    "gold_str": gold_line.split(),
                    "sparse_str": sparse_line,
                    "present_lexemes": get_present_lexemes(known_tokens, sparse_line)
                })
    
    if evaluate:
        evaluate_data(result_data)

def evaluate_data(data):
    csv_header = ['doc_id', 'orth', 'sparse', 'lexicon', 'baseline_density', 'fullword_suggestions', 'length_gold', 'len_baseline_transcriptions', "correct_partialword_suggestions"] 
    
    with open('spotted-words/data.csv', "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(csv_header)
    
        for i,doc in enumerate(data):
            num_chars_in_present_lexemes = len("".join(doc['present_lexemes']))
            num_chars_in_gold_str = len("".join(doc['gold_str']))
            
            baseline_transcription_density = num_chars_in_present_lexemes/num_chars_in_gold_str # aka, what percent of characters were already covered by transcription
            
            correct_fullword_suggestions =  set(doc['suggestions']).intersection(set(doc['gold_str']))
            correct_fullword_suggestions.difference_update(doc['present_lexemes'])
            transcription_density_accepting_fullwords = get_fullword_density(gold_toks = doc['gold_str'], found_tokens=correct_fullword_suggestions, present_lex = doc['present_lexemes'])
            
            correct_partialword_suggestions = set([x for x in doc['suggestions'] if x in " ".join(doc['gold_str'])])  # may need manual correction
            correct_partialword_suggestions.difference_update(doc['present_lexemes'])

            num_chars_in_correct_partial_suggestions = len("".join(correct_partialword_suggestions))
           
            writer.writerow(["doc" + str(i), " ".join(doc['gold_str']), doc['sparse_str'], doc['present_lexemes'], baseline_transcription_density, correct_fullword_suggestions, num_chars_in_gold_str, num_chars_in_present_lexemes, correct_partialword_suggestions])

def get_fullword_density(gold_toks, found_tokens, present_lex):
    # make string from gold tokens
    gold_str = " ".join(gold_toks)

    # remove all gold spotted tokens (1st instance only per token)
    for found in found_tokens:
        gold_str = re.sub(found, "", gold_str, count=1)

    # remove all present_lexemes if any (1st instance only per token)
    present_lex = sorted(present_lex, key=lambda x: len(x), reverse=True)
    for found in present_lex:
        gold_str = re.sub(found, "", gold_str, count=1)
    
    # define what post-transcribed density is: (how many characters left to transcribe)/(how many there were to transcribe total) 
    total_to_transcribe = len("".join(gold_toks))
    left_to_transcribe = len("".join(gold_str.split()))

    return 1 - (left_to_transcribe/total_to_transcribe)

def get_present_lexemes(known_tokens, sparse_line):
    tokens = sparse_line.split()
    return [x for x in tokens if x in set(known_tokens)]

def load_known_vocab(filepath):
    with open(filepath, "r") as f:
        lines = [x.split('\t')[0] for x in f.readlines()]
        return set(lines)

def has_overlap(list1, list2):
    return bool(set(list1) & set(list2))

if __name__ == "__main__":
    main(
        input_file="sparse-transcriptions/sparse_transcriptions_sg.top20.txt",
        known_vocab="vocabs/sg_vocab.20.txt",
        evaluate=True
        )