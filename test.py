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

    for w in words1:
        matched_lexemes = [lex for lex in liwc._lexeme2codes.keys() if fnmatch.fnmatch(w, lex)]
    # takes 17 sec

    # bigrams1 = liwc.bigrams(words1)
    # for w in bigrams1:
    #     liwc.word2codes(w)



# main
if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test1()", number=1, setup="from __main__ import test1"))
