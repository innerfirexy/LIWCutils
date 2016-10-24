# Contains the LIWCutils class
# Yang Xu
# 10/24/2016

import fnmatch
import pickle
import re
import sys

# the LIWCutils class
class LIWCutils:
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
    def count_markers(self, wl, dic):
        """
        wl: word list to be counted
        dic: a dict object whose keys are LIWC categories, and values are corresponding lexemes
        """
        # to lower
        wl = [w.lower() for w in wl]
        # combine the negation "n't" in wl to the preceding word
        wl_new = []
        i = 0
        while i < len(wl):
            if i+1 < len(wl):
                if wl[i+1] == "n\'t":
                    wl_new.append(wl[i] + wl[i+1])
                    i += 2
                else:
                    wl_new.append(wl[i])
                    i += 1
            else:
                wl_new.append(wl[i])
                break
        # count for each category
        res = {key: 0 for key in dic}
        for key, val in dic.items():
            res[key] = sum([len(fnmatch.filter(wl_new, lex)) for lex in val])
        # return
        return res

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
