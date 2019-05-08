# test.py
# Yang Xu
# 2/20/2017

from LIWCutils import LIWCdict
import fnmatch

##
# text = 'i love you'
# print(liwc.text2markers(text))
#
# liwc.word2codes('i')
# liwc.word2markers('i')
#
# ##
# refdict = liwc.sublex2codes(['article'])
# liwc.text2markers('the apple is good')



##
# test1
def test1():
    catfile = 'liwccat2007.txt'
    dicfile = 'liwcdic2007.dic'
    liwc = LIWCdict(catfile, dicfile)

    markers = ['article', 'ppron', 'ipron']
    text1 = 'you could try the tonbridge historical society URL even if the website does n\'t have more info they may have other sources listed or members might be able to help i \'m not a member'
    # liwc.text2markers(text1, markers)

    words1 = text1.split()
    codes1 = []

    # for w in words1:
    #     # liwc.word2codes(w)
    #     if w in liwc._lexeme2codes:
    #         codes1 += liwc._lexeme2codes[w]
    # print(codes1)
    # takes only 0.027 sec

    # for w in words1:
    #     matched_lexemes = [lex for lex in liwc._lexeme2codes.keys() if fnmatch.fnmatch(w, lex)]
    # takes 17 sec

    # bigrams1 = liwc.bigrams(words1)
    # for w in bigrams1:
    #     liwc.word2codes(w)

    # test search_wc_key
    # print(liwc.search_wc_key('matter'))
    # print(liwc.search_wc_key('%$%#$%'))

    # test how the new word2codes (using search_wc_key) works with text1
    for w in words1:
        # liwc.word2codes(w)
        liwc.text2markers(text1, markers)
    # word2codes takes 0.037 sec
    # text2markers takes .12 sec

##
# test2
def test2():
    catfile = 'liwccat2007.txt'
    dicfile = 'liwcdic2007.dic'
    liwc = LIWCdict(catfile, dicfile)

    # print all markers
    print('All 64 markers: ')
    print(liwc.get_markers(sort='A'))

    # print the count of lexemes corresponding to 11 markers
    markers = ['article', 'certain', 'conj', 'discrep', 'excl', 'incl', 'negate', 'preps', 'pronoun', 'quant', 'tentat']
    for m in markers:
        print('{0} # of lexemes: {1}'.format(m, len(liwc.marker_lexemes(m, include_wc=False))))
    # This is not necessarily the same as Doyle's results (ACL2016, Table 1)

    # examine certain markers
    print('\narticle lexemes: ')
    print(liwc.marker_lexemes('article', include_wc=False))

    print('\ncertain lexemes:')
    print(liwc.marker_lexemes('certain', include_wc=False))

    print('\nconj lexemes:')
    print(liwc.marker_lexemes('conj', include_wc=False))

    print('\ndiscrep lexemes:')
    print(liwc.marker_lexemes('discrep', include_wc=False))

    print('\nexcl lexemes:')
    print(liwc.marker_lexemes('excl', include_wc=False))

    print('\nincl lexemes:')
    print(liwc.marker_lexemes('incl', include_wc=False))

    print('\nnegate lexemes:')
    print(liwc.marker_lexemes('negate', include_wc=False))

    print('\npreps lexemes:')
    print(liwc.marker_lexemes('preps', include_wc=False))

    print('\npronoun lexemes:')
    print(liwc.marker_lexemes('pronoun', include_wc=False))

    print('\nquant lexemes:')
    print(liwc.marker_lexemes('quant', include_wc=False))

    print('\ntentat lexemes:')
    print(liwc.marker_lexemes('tentat', include_wc=False))

    ##
    # examine whose lexemes include single quote, e.g., we'll, they'd etc.
    print('\n')
    for m in markers:
        print('{0} single quote #: {1}'.format(m, len([w for w in liwc.marker_lexemes(m, include_wc=False) if '\'' in w])))
        print('\t' + str([w for w in liwc.marker_lexemes(m, include_wc=False) if '\'' in w]))
    # article single quote #: 0
    # certain single quote #: 3
    # conj single quote #: 0
    # discrep single quote #: 15
    # excl single quote #: 0
    # incl single quote #: 0
    # negate single quote #: 24
    # preps single quote #: 0
    # pronoun single quote #: 34
    # quant single quote #: 0
    # tentat single quote #: 1


def test_new_text2markers():
    catfile = 'liwccat2007.txt'
    dicfile = 'liwcdic2007.dic'
    liwc = LIWCdict(catfile, dicfile)

    text1 = 'you could try the tonbridge historical society URL even if the website does n\'t have more info they may have other sources listed or members might be able to help i \'m not a member'
    print('text:')
    print(text1)
    print('length of text: {}'.format(len(text1.split())))

    # Test with 14 commonly used markers
    markers_14 = ['adverb', 'article', 'auxverb', 'certain', 'conj', 'discrep', 'excl', 'incl', 'ipron', 'negate', 'ppron', 'preps', 'quant', 'tentat']

    markers = liwc.text2markers(text1, marker_limit=None, markers_incl=markers_14)
    print('markers:')
    print(markers)
    print('number of markers: {}'.format(len(markers)))

    # Test with some random text
    print()
    text2 = 'fasjdfsjf dfsfiow  fdfsdf ioioif fsdfff'
    print('text2:')
    print(text2)

    markers = liwc.text2markers(text2, marker_limit=None, markers_incl=markers_14)
    print('markers:')
    print(markers)



# main
if __name__ == '__main__':
    # test1
    # import timeit
    # print(timeit.repeat("test1()", number=1, repeat=10, setup="from __main__ import test1"))

    # test2
    # test2()

    test_new_text2markers()
