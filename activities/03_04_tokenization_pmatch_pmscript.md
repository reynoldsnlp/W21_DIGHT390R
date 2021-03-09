# Using your transducer as a tokenizer

Lauri Karttunen, one of the original pioneers of finite-state morphological
analysis, and co-author of the XFST documentation, published an
[article](https://www.researchgate.net/profile/Lauri-Karttunen/publication/221504250_Beyond_Morphology_Pattern_Matching_with_FST/links/0a85e530cdd7291013000000/Beyond-Morphology-Pattern-Matching-with-FST.pdf)
in 2011 outlining a method for using FSTs for pattern matching, including Named
Entity Recognition (NER), Relation Extraction, tokenization, and parsing. These
functionalities have been implemented in
[`hfst-pmatch2fst`](https://github.com/hfst/hfst/wiki/HfstPmatch2Fst),
[`hfst-pmatch`](https://github.com/hfst/hfst/wiki/HfstPmatch), and
[`hfst-tokenize`](https://github.com/hfst/hfst/wiki/HfstTokenize).

The pmatch algorithm is based on the "left-to-right longest-match principle",
meaning that if your FST recognizes four surface strings (`walk`, `the`, `dog`,
and `the dog`), then when tokenizing the string `walk the dog`, the output will
be `walk` and `the dog`.

> If an input symbol matches the first symbol of a pattern the pmatch algorithm
> fetches the next symbol from the input and continues as long as it can follow
> a path in the pattern network. If a valid match is found, the pmatch
> algorithm produces an output and restarts from the end of the matching
> string. If the match is unsuccessful, pmatch moves one symbol to the right
> from the previous starting point in the input and tries again.
> 
> The left-to-right longest-match principle entails that a match is valid only
> if a longer match cannot be found. If pmatch finds a longer match for a
> pattern, the output for any previously found shorter match is discarded.

In addition to using your FST, a pattern-matching script (`pmscript`) can
define regular patterns that words in your language can match, allowing the
tokenizer to effectively tokenize words that are not yet in your FST.  Most of
the work of writing a tokenizer `pmscript` has already been done for you, but
you may need to make a few tweaks, depending on your language's alphabet and
punctuation conventions.

## pmscript tweaks

Open `tools/tokenisers/tokeniser-disamb-gt-desc.pmscript` in your text editor.

### `alphabet`

The `alphabet` is declared using the keyword `Define`, so search for `Define
alphabet` in your file.  Your tokenizer already recognizes many variants of the
latin alphabet. Even if your language uses a different alphabet, it is probably
a good idea to keep the latin characters in your tokenizer, assuming that in
running text you may encounter words taken directly from English or other
latinate orthographies.

Characters are declared as spans in the unicode table in quotation marks
(`"A-Z"`) or as individual characters in curly braces (`{æ}`). All of these
declarations are separated by the pipe symbol (`|`). The `Define` statement is
terminated by a semicolon (`;`).

To determine the span of your alphabet in unicode, you can consult [the
official unicode code charts](https://unicode.org/charts/). Note that the
tables are read top-to-bottom, one column at a time. Make sure that all of the
characters you want to include are actually inside that span. If the span
includes characters that you do not want included, you can simply declare
multiple spans to skip them. For example, to skip `F`, I could declare
`"A-E"|"G-Z"`.

### `alphamiddle`

Search for `Define alphamiddle` in your pmscript. As described in the comment,
these characters can appear in the middle of the word, but not at the beginning
or end, so it will "treat `foo-bar` as one big unknown, but `-foo` (or `bar-`)
as two tokens". If your language uses something other than a hyphen to join
words, edit `alphmiddle` accordingly.


## Compiling your tokenizer

In order to build your tokenizer, pass the `--enable-tokenisers` argument (note
the British spelling) to the `configure` script.

```bash
$ ./configure --enable-tokenisers
$ make
```

Assuming that your changes to the `pmscript` file were syntactically valid, the
compiled tokenizer transducer is now at
`tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst`.

## Using your tokenizer

After compiling your tokeniser, use `hfst-tokenize` to tokenize (and optionally
analyze) running text. By default, the tokenizer segments/tokenizes without
analyzing, outputting one token per line:

```bash
$ echo "Борис бларгвит. Саша бларгвит. Все бларгвят." | hfst-tokenize tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst
Борис
бларгвит
.
Саша
бларгвит
.
Все
бларгвят
.
```

Other options and formats are available. See the documentation; use the `--help`
flag; or use `$ man hfst-tokenize` to see other options such as the following:

```
  -z, --segment            Segmenting / tokenization mode (default)
  -i, --space-separated    Tokenization with one sentence per line, space-separated tokens
  -x, --xerox              Xerox output
  -c, --cg                 Constraint Grammar output
  -S, --superblanks        Ignore contents of unescaped [] (cf. apertium-destxt); flush on NUL
  -g, --giella-cg          CG format used in Giella infrastructe (implies -l2,
                           treats @PMATCH_INPUT_MARK@ as subreading separator,
                           expects tags to start or end with +, flush on NUL)
  -C  --conllu             CoNLL-U format
  -f, --finnpos            FinnPos output
```

The most likely formats for our purposes are `--xerox` (XFST/HFST stream) and `--cg` or `--giella-cg` (Constraint Grammar stream). Example of each are below:


#### Xerox stream

```bash
$ echo "Борис бларгвит. Саша бларгвит. Все бларгвят." | hfst-tokenize --xerox tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst
Борис	Борис N Prop Sem/Ant Msc Anim Sg Nom
Борис

бларгвит

.	. CLB

Саша	Саша N Prop Sem/Ant Msc Anim Sg Nom
Саша	Саша N Prop Sem/Ant Fem Inan Sg Nom
Саша

бларгвит

.	. CLB

Все
Все	все Pron Pl Nom

бларгвят

.	. CLB 
```

#### CG stream

```bash
$ echo "Борис бларгвит. Саша бларгвит. Все бларгвят." | hfst-tokenize --cg tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst
"<Борис>"
	"Борис" N Prop Sem/Ant Msc Anim Sg Nom


"<бларгвит>"


"<.>"
	"." CLB

"<Саша>"
	"Саша" N Prop Sem/Ant Msc Anim Sg Nom
	"Саша" N Prop Sem/Ant Fem Inan Sg Nom


"<бларгвит>"


"<.>"
	"." CLB

"<Все>"

	все Pron Pl Nom

"<бларгвят>"


"<.>"
	"." CLB
```

## Process a corpus to determine which words to add next

Once you have a corpus of running text in your target language, you can easily
discover/prioritize missing words using the following idiom: (you may need to
replace `egrep "\+\?\s+inf"` with something simpler like `grep "+?"`, depending
on what version of grep you have on your operating system.

```bash
$ echo "Борис бларгвит. Саша бларгвит. Все бларгвят." | hfst-tokenize tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst | hfst-lookup -q src/analyser-gt-desc.hfst | egrep "\+\?\s+inf" | cut -f 1 | sort | uniq -c | sort -nr > todo_lexemes.tmp
```

...or with nice formatting...

```bash
$ echo "Борис бларгвит. Саша бларгвит. Все бларгвят."  \
      | hfst-tokenize tools/tokenisers/tokeniser-disamb-gt-desc.pmhfst  \
      | hfst-lookup -q src/analyser-gt-desc.hfst  \
      | egrep "\+\?\s+inf"  \
      | cut -f 1  \
      | sort  \
      | uniq -c  \
      | sort -nr  \
      > todo_lexemes.tmp
```

The output of this command, `todo_lexemes.tmp`, is a list of tokens sorted in
order of frequency:

```bash
$ cat todo_lexemes.tmp
      2 бларгвит
      1 бларгвят
      1
```

To understand what each step of the pipeline is doing, simply delete all the
subsequent commands and add ` | less` to the end.  To adapt this pipeline to
your language, you will probably work from a file or files with running text,
so instead of `echo "Words to be analyzed."`, you will use `cat my_corpus.txt`.

Now that you know which tokens cause the most problems for your FST, get to
work adding them!!! 😉
