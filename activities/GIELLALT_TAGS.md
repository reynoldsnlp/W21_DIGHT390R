# Notes about which tags to use in the GiellaLT framework

What follows is taken from a series of posts I received from Sjur Moshagen
about factors that should influence your decisions about tags to use in your
FST. He mentions [UniMorph](http://unimorph.ethz.ch/) (which is based on the
Leipzig tags) and [Universal Dependencies](https://universaldependencies.org/)
(UD) as alternatives to compare to.

## tldr;

The very short and basic answer is that automatic filtering and fst processing
will not work (i.e. no changes will be applied to the fst's), but otherwise not
much will happen. For example, if you want to use the morphology as a speller,
you (at least presently) have to adhere to the GiellaLT conventions for Error
tags.

## Full text

When looking at the details, there are several dimensions to your question. I
will try to answer them all. Please feel free to elaborate and comment - this
discussion is helping the development of the GiellaLT infra.

At least the following are relevant for discussing tagging of linguistic
content:

* the syntax of the tag strings and the tagging scheme, ie the form they take
* the tag themselves, and the meaning they represent
* the order of the tags
* restrictions of the technology being used

In addition, when comparing with UniMorph and UD, there are some
features/aspects that are not covered by one or both of them:

* normativity
* word form generation and tag optionality/irrelevance (alternatively: fst word
  form generation robustnes)
* application specific needs
* higher-level tags (syntactic relation, function, semantics, pragmatics) -
  covered by UD, but not by UniMorph

First of all, regarding the tags themselves, the tag inventory so to speak, our
work started many years earlier than both UD and UniMorph, and the set of
features conveyed by the tags are heavily influenced by established grammatical
traditions for the languages being described. We have not sought to deviate
from tradition unless there has been very good reasons for it.

When doing work on new languages, you are free to use the features and tags you
see most fit. I definitely see the point of standardisation, and I would
encourage using tags that are easily convertible to either UniMorph or UD
schemes (see below for why conversion is needed). That is, if you feel strongly
for using +NOUN instead of just +N, feel free to do that.

In defence of the present GiellaLT tag set, shorter tags mean less typing. We
also use different classes of tags in various ways by way of their form (UPPER,
Initial, lower, Prefixed/xx, etc), making it easy to distinguish between them
both when reading and processing. More on that below.

It should also be mostly trivial to convert the GiellaLT tags to both UniMorph
and UD. In fact, there has been pondering on how to add that as a form of
post-processing of the final analyses, to make the output of our tools
compatible with that of other tools and frameworks.

## Restrictions on the technology

Regarding restrictions of the technology there are two types:

* fst limitations/traditions
* Constraint Grammar (CG) syntax expectations - this is only relevant if you
  plan to use CG in your project

### FST limitations/traditions

When building an fst, you usually make a distinction between the surface form,
the lemma and the tags. The tags are multichar symbols (technically, they don't
have to be, but not declaring them as multichars will lead to all sorts of
debugging and processing issues, so it is not a good idea). That is:

* surface form: string of individual symbols (ie letters, except perhaps for
  letters made with combining diacritics)
* lemma: string of individual symbols/letters
* analysis tags: one or more multichar symbol, usually separated from the lemma

This is all trivial, and you can implement both UniMorph tag syntax or UD
tagging schemes using an fst, although the tabular syntax of UD makes it a bit
cumbersome to work with in an fst setting. We have been mostly following the
tagging scheme documented in the Xfst book (Finite State Morphology, Kenneth R.
Beesley and Lauri Karttunen, CSLI Publications, 2003) — the FST "bible". More
on the tag syntax below.

### Constraint Grammar (CG) syntax restrictions

In CG, everything is a tag, and tags are space separated. There are further
expectations regarding tags for syntactic functions and syntactic relations.
Our take on this that we adhere to (and convert from the Xerox tags mentioned
above to) CG tagging as part of our pipelines. This is done automatically if
you use the GiellaLT (ie Xerox) tag syntax (and again: more on tag syntax
below).

Regarding tag order, we follow the same principle as UD and UniMorph (UM):
order is fixed. The order is more or less the same as in both UD and UM, so
conversion should be trivial in most cases.

There are linguists that would like tag order to reflect morph order in the
surface string. It is possible within our infra to build such analysers, but
the expectation is then that the linguist also provides a script to reorder the
tags to a fixed order, for tools that expect it (most tools do, as well as most
of the provided test features).

Regarding the syntax of the tag strings and the tagging scheme, the GiellaLT
assumes one default syntax, but can convert to multiple other schemes &
syntaxes.

## Default syntax (aka GiellaLT tags, GT tags, Xerox tags)

* tag separator: + — for prefix tags, the separator follow the tag, for suffix
  tags it precedes the tag; infix tags are discouraged (see below)
* POS tags: Init case (e.g. Adv)
* SUBPOS tags: Init case (e.g. Prop)
* feature tags: Init case/mixed case
* Tags optional for generation: tag prefix Gram/
* Semantic tags: tag prefix Sem/
* tags for specific applications: tag prefix Use/ (see also below)
* error tags (ie violation of a norm): tag prefix Err/

### Other supported tag syntaxes (conversion to these formats from GT is mostly automatic)

* CG compatible GiellaLT tags: the + separator is automatically converted to a
  space, compounds are rendered using sub-readings, to make only the last part
  of the compound visible to the default CG processing
* Apertium tags: Apertium encapsulates all tags in <>, and use only lowercase.
  FST's intended for use with Apertium are automatically converted to this
  format, with optional hand conversion of certain tags

The tag format being used is indicated in the fst filename:

* `analyser-mt-apertium-desc.hfst` — `-mt-` shows it is used for Machine
  Translation, `-apertium-` that it is using the Apertium tagging syntax
* `analyser-mt-gt-desc.hfst` — as above, but using the GiellaLT (`-gt-`)
  tagging syntax

### Conversion to other tagsets

It is quite trivial to add automatic conversion to other tagging schemes.
Conversion to UD is more convoluted, as one also would want syntactic relations
and dependencies to be encoded. But as mentioned above, people are looking into
this.

Supporting other default tagging schemes is not possible today, mainly due to
automatic filtering and filter generation. Examples of automatic filtering are:

* remove semantic tags from all fst's except those used for disambiguation and
  syntactic parsing
* remove erroneous strings from fst's used for spelling and similar normative
  tasks
* remove area specific strings from an fst intended for another area

These filters are automatically generated from the set of multichar symbols in
the fst, and presently only tags of the form `+Tag` or `Tag+` are recognised.
If one use other tagging schemes, the filtering will not work. This may be a
problem, or it may not.

One could consider adding support for more source code tagging formats, but
that is a non-trivial task that will add to the complexity of the
infrastructure.

## Normativity

The GiellaLT infra is written with a very broad application in mind: it should
be equally useful for general linguistic work (language description, analysis)
as for specific applications (more on applications below). One of the core
applications are proofing tools. That is: have I written language X correctly
according to some standard or prescriptive grammar/dictionary?

This question will often be considered crucial for language (re)vitalisation
work, and supporting that has been core to the development of the GiellaLT
infra. We use error tags (see above) to tag strings outside the normative
space.

Normativity is not even mentioned in the UniMorph reference article
(https://unimorph.github.io/doc/unimorph-schema.pdf), and I assume the same is
true for UD - they are both about describing language, not prescribing language
use.

Given that most work on minority and indigenous languages are under-resourced,
there is no room for doing double up – one normative and one descriptive.
Instead we have to accomodate both within the same source, and generate one or
the other through automatic means. This is supported by the GiellaLT infra, but
only if one is using the GiellaLT tagging syntax, at least for the "Error"
part.

There is a separate discussion on whether we need to make the normativity
distinctions more fine grained (see
https://giella.zulipchat.com/#narrow/stream/124588-all_langs/topic/Different.20flavours.20of.20spellrelax),
but that does not change the need to follow GiellaLT tagging standards to get
the correct normativity behavior.

## Word form generation

Many of the applications supported by the GiellaLT infra requires word form
generation. In the FST world, that means that the generation input (ie lemma +
analysis string) matches exactly the string recognised by the fst - or you will
get nothing.

In practice this means that you need a fixed tag order (see above), but you
also need some classes of tags to be optional: What transitivity does verb X
have? If you don't know, and the transitivity (or similar) tag is required for
generation, then you will often be without luck. And in many languages,
although transitivity is important for syntactic parsing, it is usually
completely irrelevant to morphology. The fst way of handling this is by making
such tags optional - good if you know, and fine if you don't.

To be able to do this for all languages, we need to distinguish between tags
important for word form generation, and tags that are irrelevant. The general
pattern in the GiellaLT infra is that we use prefixed tags for things
irrelevant to generation, making it trivial to generate filters that make these
tags optional, or even remove them.

For this to work, one obviously need to adhere to the GiellaLT tagging scheme.

## Application-specific needs

Since the GiellaLT infra is as much focused on creating tools for the language
communities as it is on lingustic analysis and understanding, we have a set of
tags used to modify fst's for specific applications. Example: in MT we want to
avoid two parallel forms to be generated, so we have a tag saying «do not
generate this form» there are usually some words that should never be suggested
by the speller, and we have a tag for indicating that. There is no place for
such additional information within the UD or UM frameworks — and there should
not be, as they serve a different purpose. But within the GiellaLT infra we
need these tags for many of the languages developed here.

## Higher-level tags

The GiellaLT infrastructure supports higher-level analysis using Constraint
Grammar, all the way up to semantic parsing. We have been using CG due to the
rule-based nature of the formalism, and the quite relaxed approach to
incomplete processing: within the CG world there is no problem if a syntactic
tree is not complete, or some ambiguity is left as is.

This works well in real-world applications, and the CG formalism has been used
successfully in many advanced NLP tasks and tools.

UM does not support higher-level tags. UD does very much, but with a different
tag syntax.

As mentioned above, CG has its own expectations for tags for syntactic
functions and relations, but are otherwise quite flexible. One can e.g. use CG
grammars with Apertium tags.

## Conclusion

* standardisation is a good thing, and it is a long-term goal that all tags
  used within the GiellaLT infra can be mapped 1:1 to UM or UD or both.
* there is a difference between tag form or syntax, and the tag content or text
  string
* it is advisable to follow the GiellaLT tag syntax
* the tag text can still follow UM or UD, to retain 1:1 mapping with them
