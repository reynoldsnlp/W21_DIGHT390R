# ISO 639-3 codes

For naming new language repositories, the Giellatekno infrastructure follows
[BCP47](https://en.wikipedia.org/wiki/IETF_language_tag), but always using ISO
639-3 codes instead of 639-1.

* https://en.wikipedia.org/wiki/ISO_639-3
* https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes

Most wikipedia articles about languages have the ISO 639-3 code in the table
on the right.


# Weights

In lexc, one can assign weights to entries in a lexicon that are summed to a
final weight for a reading. Weights can be positive or negative. In the
following example, the weights assigned match the surface forms, so we can
easily see what happens when we apply weights.

```lexc
LEXICON Root
stems ;

! We use the gloss syntax to add weights using the keyword "weight"
! Glosses and weights can be declared side by side
LEXICON stems
s1 endings "weight: 1.0, gloss: word1" ;
s2 endings "weight: 2.0, gloss: word2" ;
s3 endings "weight: 3.0" ;
s-1 endings "weight: -1.0, gloss: word1" ;
s-2 endings "weight: -2.0, gloss: word2" ;
s-3 endings "weight: -3.0" ;

LEXICON endings

e1 # "weight: 1.0" ;
e2 # "weight: 2.0" ;
e3 # "weight: 3.0" ;
e-1 # "weight: -1.0" ;
e-2 # "weight: -2.0" ;
e-3 # "weight: -3.0" ;
```

After compiling the transducer (`hfst-lexc weights.lexc > weights.hfst`) we can
see the resulting weights by using `hfst-lookup`:

```
$ hfst-lookup weights.hfst
hfst-lookup: warning: It is not possible to perform fast lookups with OpenFST, std arc, tropical semiring format automata.
Using HFST basic transducer format and performing slow lookups
> s-1e1
s-1e1	s-1e1	0.000000

> s-1e2
s-1e2	s-1e2	1.000000

> s-2e3
s-2e3	s-2e3	1.000000

> s-3e-3
s-3e-3	s-3e-3	-6.000000
```

Weights can be leveraged at a various levels of your processing pipeline, but
this is usually done in one of two ways. First, by `hfst-lookup` using the
`-b/--beam B` flag, which outputs only analyses whose weight is within `B` from
the best analysis. Typically, the value of `B` is 0. Second, constraint grammar
rules can be used to limit readings by weights. We will discuss how to do this
later when we learn about constraint grammars.

> EXERCISE 1: Write a minimal lexc file that gives more weight to verb forms
> that are homonymous with nouns, e.g. `work+V+Prs+3sg:works` should have a
> higher weight than `work+N+Pl:works`.

# Intro to GiellaLT framework

https://github.com/giellalt/lang-rus
