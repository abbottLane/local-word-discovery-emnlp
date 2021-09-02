import os
import re
from HFST_Model import HFSTModel

HFST_MODEL = HFSTModel("evaluation/transducers/segmenter-morph.hfst")

def main():
    files_with_orth_transcriptions = "evaluation/orth_transcriptions_sg"
    output_file = "evaluation/vocabs/sg_vocab.txt"


    morphs_dict = {}
    for i, filepath in enumerate(os.listdir(files_with_orth_transcriptions)):
        with open(os.path.join(files_with_orth_transcriptions, filepath), "r") as f:
            line = f.readline()
            lines = line.split()
            print("Processing file: " + str(filepath) + " " + str(i) )
            for l in lines:
                result = HFST_MODEL.apply_down(l)
                for r in result:
                    morphs = r.split("^")
                    for m in morphs:
                        if m in morphs_dict:
                            morphs_dict[m] += 1
                        else:
                            morphs_dict[m] = 1
    with open(output_file, "w") as g:
        for k,v in sorted(morphs_dict.items(), key=lambda item: item[1]): 
            g.write(k + "\t" + str(v) + "\n")




        

if __name__ == "__main__":
    main()