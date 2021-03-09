"""
Creates a corpus from Wikipedia dump file.
Copied from: (with minor edits)
https://www.kdnuggets.com/2017/11/building-wikipedia-text-corpus-nlp.html
Inspired by:
https://github.com/panyang/Wikipedia_Word2vec/blob/master/v1/process_wiki.py

Usage: python wikipedia2corpus.py "...-latest-pages-articles.xml.bz2" output-filename.txt
"""
import sys

from gensim.corpora import WikiCorpus


def make_corpus(input_filename, output_filename):
    """Convert Wikipedia xml dump file to text corpus"""
    output = open(output_filename, 'w')
    wiki = WikiCorpus(input_filename)

    i = 0
    for text in wiki.get_texts():
        output.write(bytes(' '.join(text), 'utf-8').decode('utf-8') + '\n')
        i = i + 1
        if (i % 10000 == 0):
            print('Processed ' + str(i) + ' articles')
    output.close()
    print('Processing complete!')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python make_wiki_corpus.py <wikipedia_dump_file> <processed_text_file>')
        sys.exit(1)
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    make_corpus(input_filename, output_filename)
