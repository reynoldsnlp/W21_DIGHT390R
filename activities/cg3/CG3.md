# Constraint grammar

You are probably already familiar with the concept of "generative" grammar,
which seeks to formally describe everything that is possible in a language, and
no more.  A Constraint Grammar takes the opposite approach, describing what is
***NOT*** possible in a language. This is useful for dealing with an analysis
stream that has morphological ambiguity (i.e., more than one reading per
token). The overall strategy then becomes...

1.) `Analyzer` (in our case, an FST) gives every possible reading
1.) `Constraint Grammar` removes as many ambiguous readings as possible.

## English example

Consider the following English example. The words `to`, `look` and `bear` are
morphologically ambiguous, since they each have more than one reading. Try to
think like a constraint grammar; how could you remove ambiguity based on the
context of the surrounding words?

```
"<They>"
    "they" <*> PRON PERS NOM PL3 SUBJ
"<went>"
    "go" V PAST VFIN
"<to>"
    "to" INFMARK>
    "to" PREP
"<the>"
    "the" DET CENTRAL ART SG/PL
"<zoo>"
    "zoo" N NOM SG
"<to>"
    "to" INFMARK>
    "to" PREP
"<look>"
    "look" V INF
    "look" N SG
"<at>"
    "at" PREP
"<the>"
    "the" DET CENTRAL ART SG/PL
"<bear>"
    "bear" N NOM SG
    "bear" V INF
    "bear" V PRS NON2
"<.>"
```

#### Very basic introduction

https://wiki.apertium.org/wiki/Constraint_Grammar

#### Full documentation

https://visl.sdu.dk/cg3.html

## Rules for our English sentence

One possible constraint that is true for many languages is that verbs cannot
be directly preceded by determiners. In our sentence, `bear` is directly
preceded by `the`, which rules out the possibility of `bear` being a verb.
To formalize this constraint, we need to define the context:

```
( -1 DET )
```

This context pattern says the word preceding the current word contains at least
one reading with the `DET` tag. This might be too imprecise, since the previous
word could contain other readings as well. To make this more precise, we can
specify that *ALL* of the readings on the previous word must contain the `DET`
tag by adding `C` to the location:

```
( -1C DET )
```

Now we can use this context in a `REMOVE` rule:

```
REMOVE ( V ) IF ( -1C DET ) ;
```

This rule removes all readings that contain the `V` tag from the current word
if all the remaining readings on the previous word contain the `DET` tag.
Another way to formulate this (albeit more clumsily in more complicated
sentences) is with a `SELECT` rule. These rules eliminate all readings that do
not match the given pattern:

```
SELECT ( N ) IF ( -1C DET ) ;
```

How could this `SELECT` rule go wrong?

> PRACTICE: Write a rule to remove the `INFMARK>` tag from `"to"` before `"the"`

## Running a constraint grammar using `vislcg3`

Save a txt file called `example.cg3` with the following two rules:

```
REMOVE ( V ) IF (-1C (DET)) ;

REMOVE (INFMARK>) IF (0 (PREP)) (1C (DET)) ;
```

The `vislcg3` command takes its grammar file after the `-g` flag. Our example
sentence is CG3 stream format is in `eng_cg3_stream.txt`, so the following
command will run this sentence through the constraint grammar in `example.cg3`:

```bash
$ cat eng_cg3_stream.txt | vislcg3 -g example.cg3
```

If you want to see which rules did what, you can add the `-t` or `--trace` flag
to leave eliminated readings in the stream (prefixed by `;` and suffixed with
the rule that caused it to be eliminated).

```bash
$ cat eng_cg3_stream.txt | vislcg3 -t -g example.cg3
```

Ultimately, the following pipelines are common approaches:

```bash
$ cat my_corpus.txt | hfst-tokenize --giella-cg path-to-tokenizer.pmhfst | vislcg3 -g my_grammar.cg3 > annotated_corpus.txt

...or...

$ cat my_corpus.txt | hfst-tokenize path-to-tokenizer.pmhfst | hfst-lookup -q path/to/analyser.gt-desc.hfstol | cg-conv -fC | vislcg3 -g my_grammar.cg3 > annotated_corpus.txt
```

## Where to put your `cg3` file in GiellaLT framework

For disambiguation, your `cg3` file should be saved as
`src/cg3/disambiguation.cg3`. There is already a `cg3` file there that you can
replace/adapt.
