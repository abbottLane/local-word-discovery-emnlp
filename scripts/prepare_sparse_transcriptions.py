import os
import re

orth_dir = "evaluation/orth_transcriptions_sg"
allo_dir = "evaluation/allo_transcriptions_sg"
out_dir = "evaluation/sparse-transcriptions"
vocab = "evaluation/vocabs/sg_vocab.20.txt"

def main():
    lines = []
    for i, filepath in enumerate(os.listdir(orth_dir)):
        allo_line = ""
        orth_line = ""
        allo_path = re.sub(".txt", ".wav.allo.txt", filepath)
        with open(os.path.join(allo_dir,allo_path), "r") as g:
            allo_line = g.readline()
        with open(os.path.join(orth_dir, filepath), "r") as f:
            orth_line = f.readline()
        lines.append({"filename": filepath, "allo": allo_line, "orth": orth_line})

    with open(os.path.join(out_dir, "sparse_transcriptions_sg.txt"), "w") as h:
        for l in lines:
            h.write(l['allo'])
            h.write(l['orth'])
            h.write("\n\n")
    
        


if __name__ == "__main__":
    main()