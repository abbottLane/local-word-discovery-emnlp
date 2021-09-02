## Local Word Discovery V1
This repo contains the FST implmentation of Local Word Discover for Kunwinjku, along with some scripts and output files used in the evaluation for our EMNLP 2021 paper: Local Word Discovery for Interactive Transcription.

Prerequisite: python ~3.7 environment with the `hfst` python library installed. 

To run the evaluation script: `python find_words.py` . This script will use the grammar at `kunwok-acceptor.min.bin.hfst` to spot words on `sparse-transcriptions/sparse_transcriptions_sg.top20.txt` using the Known vocabulary at `"vocabs/sg_vocab.20.txt"`. This produces results in a file at `spotted_words/data.csv`.

The implementation of the FST for word discovery can be seen in `grammar/kunwok-acceptor.xfst`. In particular the last line, `regex  [[[ "-":? ]* [0:" "] [FullGrammar .o. wspace].l [0:" "] [ "-":? ]*] .o. NoisyPhones].i;`, extends what is otherwise a standard morphological analyzer to spot possible words in a string of phones, given a certain phonemic flexibility. Spotted words are printed in the output, with characters not belonging to the spotted word transduced to the `-` symbol. 

One shortcoming of this approach is that the FST assumes that the known lexemes are aligned and imputed into the phone sequence. Further word will explore ways of doing local word discovery without explicit alignments provided a priori.  

A more user-friendly python implementation of LWD is currently under development. Check back later for a link to that work.