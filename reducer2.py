#!/usr/bin/env python

import math
import sys


class Word ():
    def __init__ (self, term):
        self.term = term
        self.docs = {}
        self.cooc = {}
        self.df = 0
        self.idf = 0.0


    def add (self, kind, val):
        co_term, doc_id = None, None
        if kind == "f":
            tf, doc_id = val.split("\t")
            self.docs[doc_id] = float(tf)

        elif kind == "c":
            #print val
            co_term, doc_id = val.split("\t")
            if co_term not in self.cooc:
                self.cooc[co_term] = set()
            self.cooc[co_term].add(doc_id)

        else:
            print "\t".join([self.term, kind, val])


    def emit (self, n_docs):
        n = len(self.docs)
        max_tfidf = 0.0

        if n > 0:
            ## emit term IDF
            self.df = float(n)
            self.idf = math.log(float(n_docs) / self.df)
            print "\t".join([self.term, "i", "%.5f" % self.idf, str(n)])

            ## emit co-occurrence probability for a term pair
            for co_term, c in self.cooc.items():
                prob_cooc = float(len(c)) * self.df / float(n_docs)
                print "\t".join([self.term, "p", co_term, "%.5f" % prob_cooc])

            ## emit term TF-IDF
            for doc_id, weight in self.docs.items():
                tfidf = weight * self.idf
                max_tfidf = max(max_tfidf, tfidf)
                print "\t".join([self.term, "t", "%.5f" % tfidf, doc_id])

            ## emit maximum term TF-IDF across all its docs, for threshold downstream
            print "\t".join([self.term, "m", "%.5f" % max_tfidf])


def main (n_docs):
    word_list = {}
    #f = open("data/head5000.txt", "r")
    #for line in f:
    for line in sys.stdin:
        line = line.strip()
       # print line
        try:
            l = line.split("\t", 2)
            word, kind, val = l

            if word not in word_list:
                w = Word(word)
                word_list[word] = w
            else:
                w = word_list[word]
            if len(val) < 50:
                w.add(kind, val)


        except ValueError, err:
            sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": str(l)})

    ## emit results
    for word, w in word_list.items():
        w.emit(n_docs)


if __name__ == "__main__":
    n_docs = 517401 # int(sys.argv[1])
    main(n_docs)
