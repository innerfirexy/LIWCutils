# Contains the LIWCdict class
# Yang Xu
# 10/24/2016

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import fnmatch
import pickle
import re
import sys
import itertools
import collections


# the LIWCdict class
class LIWCdict(object):
    def __init__(self, catfile, dicfile):
        """
        catfile: the LIWC category file, e.g., liwccat2007.txt
        dicfile: the LIWC dictionary file, e.g., liwcdic2007.dic
        """
        assert isinstance(catfile, str)
        assert isinstance(dicfile, str)

        self._catfile = catfile
        self._dicfile = dicfile

        self._code2marker = {}
        self._marker2code = {}
        with open(catfile, 'r') as fr:
            text = ''.join(fr.readlines())
            ms = re.findall(r'[0-9]+\t[a-z]+@', text)
            for m in ms:
                code, marker = m[:-1].split('\t')
                code = int(code)
                self._code2marker[code] = marker
                self._marker2code[marker] = code

        self._code2lexemes = {}
        self._lexeme2codes = {}
        self._lexemes = {} # lexemes w/o wildcard
        self._lexemes_wc = {} # lexemes w/ wildcard
        self._lexemes_wc_keys = [] # store the keys of _lexemes_wc

        with open(dicfile, 'r') as fr:
            for line in fr:
                line = line.strip()
                items = line.split('\t')
                lexeme = items[0]
                try:
                    codes = [int(c) for c in items[1:]]
                except Exception as e:
                    print(line)
                    raise
                else:
                    self._lexeme2codes[lexeme] = codes
                    for c in codes:
                        if c in self._code2lexemes:
                            self._code2lexemes[c].append(lexeme)
                        else:
                            self._code2lexemes[c] = [lexeme]
                    # add to _lexemes and _lexemes_wc
                    if '*' in lexeme:
                        self._lexemes_wc[lexeme] = codes
                    else:
                        self._lexemes[lexeme] = codes
        # sort _lexemes_wc_keys alphabetically (the default liwcdic2007.dic is already sorted)
        self._lexemes_wc_keys = sorted(self._lexemes_wc.keys())


    # binary search within _lexemes_wc_keys
    def search_wc_key(self, word):
        """
        word: a str object
        """
        first = 0
        last = len(self._lexemes_wc_keys) - 1

        while first <= last:
            mid = (first + last) // 2
            if fnmatch.fnmatch(word, self._lexemes_wc_keys[mid]):
                return self._lexemes_wc[self._lexemes_wc_keys[mid]]
            else:
                if word < self._lexemes_wc_keys[mid]:
                    last = mid - 1
                else:
                    first = mid + 1
        return None


    # the func that counts the number of LIWC markers
    def count_marker(self, material, marker, sep=' '):
        """
        material: str, a piece of text
        marker: str, marker
        """
        assert isinstance(material, str) and len(material)>0
        assert isinstance(marker, str) and self.is_marker(marker)

        lexemes = self.marker_lexemes(marker)
        unigrams = material.split(sep)
        if len(unigrams) > 1:
            bigrams = self.bigrams(unigrams)
            return self._count_list(unigrams, lexemes) + self._count_list(bigrams, lexemes)
        else:
            return self._count_list(unigrams, lexemes)


    # the func that counts in batch
    def count_marker_batch(self, material, markers, sep=' '):
        """
        """
        results = []
        unigrams = material.split(sep)
        if len(unigrams) > 1:
            bigrams = self.bigrams(unigrams)
            for m in markers:
                assert self.is_marker(m)
                lexemes = self.marker_lexemes(m)
                results.append(self._count_list(unigrams, lexemes) + self._count_list(bigrams, lexemes))
        else:
            for m in markers:
                assert self.is_marker(m)
                lexemes = self.marker_lexemes(m)
                results.append(self._count_list(unigrams, lexemes))
        return results


    # the func called in marker_count
    def _count_list(self, words, lexemes):
        """
        words: [str], a list of nigrams or bigrams
        lexemes: [str], a list of lexemes
        """
        assert isinstance(words, list)
        assert isinstance(lexemes, list)

        return sum([len(fnmatch.filter(words, lex)) for lex in lexemes])


    # generate bigrams list from unigram list
    def bigrams(self, unigrams):
        """
        unigrams: [str]
        """
        assert isinstance(unigrams, list) and len(unigrams)>1
        bigrams = []
        for i in range(len(unigrams)-1):
            bigrams.append(unigrams[i] + unigrams[i+1])
        return bigrams


    # check if marker is valid
    def is_marker(self, marker):
        """
        marker: str
        """
        assert isinstance(marker, str)
        return marker in self._marker2code


    # check if code is valid
    def is_code(self, code):
        """
        code: str
        """
        assert isinstance(code, int)
        return code in self._code2marker


    # check if a word is a valid lexeme
    def is_lexeme(self, word):
        """
        word: str
        """
        assert isinstance(word, str)
        return word in self._lexeme2codes


    # return the subset of self._lexeme2codes, by including a subset of markers only
    def sublex2codes(self, markers):
        """
        markers: the markers of the lexemes to be included
        """
        assert isinstance(markers, list)
        for i, m in enumerate(markers):
            if not self.is_marker(m):
                raise Exception('invalid param: markers[{}], {}'.format(i, m))
        # get the subset
        lexemes = itertools.chain.from_iterable(self._code2lexemes[self._marker2code[m]] for m in markers)
        subdict = {lex: self._lexeme2codes[lex] for lex in lexemes}
        return subdict


    # return the codes of a word
    def word2codes(self, word):
        """
        word: str
        """
        assert isinstance(word, str)
        if word in self._lexemes:
            return self._lexemes[word]
        else:
            codes = self.search_wc_key(word)
            return codes


    # return the markers (short) of a word
    def word2markers(self, word):
        """
        word: str
        """
        assert isinstance(word, str)
        codes = self.word2codes(word)
        if codes is None:
            return None
        else:
            return [self.code2marker(c) for c in codes]


    # the func that get the corresponding lexemes of certain markers
    def marker_lexemes(self, marker, include_wc=True):
        """
        marker: string of LIWC marker (short version)
        include_wc: include wildcard lexemes or not
        return: a list of str representing the lexemes, when marker is valid. Otherwise, return None
        """
        assert isinstance(marker, str)
        if marker in self._marker2code:
            lexemes =  self._code2lexemes[self._marker2code[marker]]
            if include_wc:
                return lexemes
            else:
                return [w for w in lexemes if w not in self._lexemes_wc]
        else:
            return None


    # the func that convert a marker string (short version) to its LIWC code
    def marker2code(self, marker):
        """
        marker: a string of LIWC marker (short version)
        return: an int representing the code
        """
        assert isinstance(marker, str)
        if marker in self._marker2code:
            return self._marker2code[marker]
        else:
            return None


    # the func that convert a LIWC code to its marker string (short or full version)
    def code2marker(self, code):
        """
        code: an int of marker code
        return: a str representing the marker
        """
        assert isinstance(code, int)
        if code in self._code2marker:
            return self._code2marker[code]
        else:
            return None


    # the function that return a piece of text to a series of makers
    def text2markers(self, text, markerfilter=None):
        """
        text: str
        refdict: a list of str
        """
        assert isinstance(text, str)
        if markerfilter is not None:
            assert isinstance(markerfilter, collections.Iterable)
            for i, m in enumerate(markerfilter):
                if not self.is_marker(m):
                    raise Exception('invalid param: markerfilter[{}], {}'.format(i, m))

        # get the marker series
        markers = []
        unigrams = text.split()
        for word in unigrams:
            ms = self.word2markers(word)
            if ms is not None:
                markers.append(ms)
        if len(unigrams) > 1:
            bigrams = self.bigrams(unigrams)
            for word in bigrams:
                ms = self.word2markers(word)
                if ms is not None:
                    markers.append(ms)

        markers = list(itertools.chain.from_iterable(markers))
        if markerfilter is not None:
            markers = [m for m in markers if m in markerfilter]
        return markers

    ##
    # Get all the lemmas of a marker
    # def get_lemmas(self, marker):
    #     assert isinstance(marker, str)
    #     if not self.is_marker(m):
    #         raise Exception('invalid param: "{}" is not a marker'.format(marker))
    #
    #     pass


    # get all markers
    def get_markers(self, sort=None):
        if sort=='A':
            return sorted(self._marker2code.keys())
        elif sort=='D':
            return sorted(self._marker2code.keys(), reverse=True)
        else:
            return list(self._marker2code.keys())
