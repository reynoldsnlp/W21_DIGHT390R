# GiellaLT framework

Many topics about the GiellaLT framework are explained here:
https://giellalt.uit.no/infra/Infrastructure.html 

## Language repository structure

Files that you will frequently use or edit are marked with `***`.

```
.
├── AUTHORS           # Add your name here
├── LICENSE           # If you don't like GPL3 license, change this
├── README.markdown   # This is the "front page" of the github website
├── autogen.sh        # Run this after you first clone the repository
├── config.log        # Here you can see how you last `configure`d
├── configure ***     # Run this after autogen.sh, and any time you change any Makefile.am  (`$ ./configure`)
├── docs              # Automatically generated documentation (based on special comments in your lexc: https://giellalt.uit.no/infra/infraremake/In-sourceDocumentation.html)
│   └── ...
├── src               # All source files for the FST, Constraint Grammars, etc.
│   ├── Makefile.am
│   ├── *.hfst        # After running `make`, compiled transducers are saved here
│   ├── cg3           # Constraint Grammar source files  (to disambiguate tokens with more than one reading)
│   │   ├── Makefile.am
│   │   ├── dependency.cg3  # Add dependency labels (syntactic structure)
│   │   └── disambiguator.cg3 ***  # The main CG3 file for disambiguating
│   ├── fst           # Source (and after `make`, compiled transducers) for building the main FST
│   │   ├── Makefile.am ***  # Declare which lexc files to use
│   │   ├── affixes      # Lexc files for affix continuation classes
│   │   │   └── *.lexc
│   │   ├── generated_files  # Automatically generated files for punctuation, etc.
│   │   │   ├── 00README.txt
│   │   │   ├── punctuation.lexc
│   │   │   └── symbols.lexc
│   │   ├── incoming         # Place to save any (non-copyrighted) materials to help build the FST
│   │   │   ├── 00README.txt
│   │   │   └── ...
│   │   ├── phonology.twolc ***  # Two-level phonology source file
│   │   ├── root.lexc ***    # Root lexc file. Contains Multichar_Symbols and LEXICON Root
│   │   ├── stems            # Lexc files for lexemes
│   │   │   └── *.lexc ***
│   │   └── url.hfst
├── test
│   ├── data
│   │   └── typos.txt  # typos and their corrections (to test spell-checker)
│   ├── src
│   │   ├── Makefile.am ***  # List/unlist tests that you expect to fail
│   │   ├── dict-gt-yamls
│   │   │   ├── dicttests_dict-gt-desc.ana.yaml
│   │   │   └── dicttests_dict-gt-norm.gen.yaml
│   │   ├── gt-desc-yamls ***  # Add directories like this to test specific flavors of your FST
│   │   │   └── *.yaml
│   │   ├── morphology  # For testing lemma generation
│   │   │   ├── Makefile.am  # List/unlist tests that you expect to fail
│   │   │   ├── generate-adjective-lemmas.sh.in   # Define tags that go with dictionary form
│   │   │   ├── generate-noun-lemmas.sh.in        # Define tags that go with dictionary form  
│   │   │   ├── generate-propernoun-lemmas.sh.in  # Define tags that go with dictionary form
│   │   │   ├── generate-verb-lemmas.sh.in        # Define tags that go with dictionary form
│   │   │   └── tag_test.sh  # Tests whether there are tags that are not listed in Multichar_Symbols in root.lexc
│   │   ├── phonology  # I am not familiar with how these work. Might be useful!
│   │   │   ├── Makefile.am
│   │   │   ├── pair-test-hfst.sh.in
│   │   │   ├── pair-test-negative.sh.in
│   │   │   └── pair-test-positive.sh.in
│   │   └── syntax
│   │       └── Makefile.am
├── tools
│   ├── Makefile.am
│   ├── spellcheckers
│   │   └── Makefile.am
│   └── tokenisers
│       ├── Makefile.am
│       ├── corpustags.txt
│       ├── mwe-dis.cg3
│       ├── paradigm.abbr.txt
│       └── tokeniser-disamb-gt-desc.pmscript  # Define alphabet, etc. for tokenizer
```
