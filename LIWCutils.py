# Contains the LIWCdict class
# Yang Xu
# 10/24/2016

import fnmatch
import pickle
import re
import sys

# the LIWCdict class
class LIWCdict(object):
    def __init__(self, cat_file, dic_file):
        """
        cat_file: the LIWC category file, e.g., liwccat2007.txt
        dic_file: the LIWC dictionary file, e.g., liwcdic2007.dic
        """
        assert isinstance(cat_file, str)
        assert isinstance(dic_file, str)

        self._catfile = cat_file
        self._dicfile = dic_file

        self._code2marker = {}
        self._marker2code = {}
        with open(cat_file, 'r') as fr:
            text = ''.join(fr.readlines())
            ms = re.findall(r'[0-9]+\t[a-z]+@', text)
            for m in ms:
                code, marker = m[:-1].split('\t')
                code = int(code)
                self._code2marker[code] = marker
                self._marker2code[marker] = code

        self._code2lexemes = {}
        self._lexeme2codes = {}
        with open(dic_file, 'r') as fr:
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
            bigrams = self.bigrams(nigrams)
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
                lexemes = self.marker_lexemes(m)
                results.append(self._count_list(unigrams, lexemes) + self._count_list(bigrams, lexemes))
        else:
            for m in markers:
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
        words = [w.lower() for w in words]
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

    # the func that get the corresponding lexemes of certain markers
    def marker_lexemes(self, marker):
        """
        marker: string of LIWC marker (short version)
        return: a list of str representing the lexemes, when marker is valid. Otherwise, return None
        """
        assert isinstance(marker, str)
        if marker in self._marker2code:
            return self._code2lexemes[self._marker2code[marker]]
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
        assert isinstance(marker, int)
        if code in self._code2marker:
            return self._code2marker[code]
        else:
            return None
