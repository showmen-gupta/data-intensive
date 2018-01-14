#!/usr/bin/env python

import hashlib
import re
import sys

def getStopWords(stopword_src):
    stopwords = set([])
    if stopword_src:
        f = open(stopword_src, "r")
        try:
            for line in f:
                line = line.strip()
                stopwords.add(line)

        except ValueError, err:
            sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": line})
        f.close()
    return stopwords


def getUUID(msg_uri):
    return hashlib.md5(msg_uri).hexdigest()

def parseMsg(body):
    regex1 = r'(\b(?=\w*[@\.])[\w\-\.@]+\b)'
    regex2 = r'[0-9]+'
    regex3 = r'[^a-z0-9\-\_]'
    pat = r'^[\-\_]+$'
    term_count = {}
    word_bag = set([])
    body = re.sub(regex1, " ", body)
    l = re.sub(regex3, " ", body.strip().lower()).split(" ")
    for word in l:
        word = re.sub(regex2, "", word).strip()
        if not re.search(pat, word) and (len(word) > 0) and (len(word) < 50):
            # term counts within a doc
            if word not in term_count:
                term_count[word] = 1
            else:
                term_count[word] += 1
            word_bag.add(word)
    return term_count, word_bag


def getTermList(word_bag):
    term_list = list(map(lambda x: x, word_bag))
    term_list.sort()
    return term_list


def getTermFreq(term_count, term_list):
    sum_tf = float(sum(term_count.values()))
    term_freq = {}
    for i in range(0, len(term_list)):
        word = term_list[i]
        term_freq[word] = float(term_count[word]) / sum_tf
    return term_freq


def emit(msg_uri, doc_id, date, send, recv, term_list, term_freq, stopwords):
    # emit document (email message) metadata
    print "\t".join([doc_id, "d", msg_uri, date])
    # emit sender/receiver social graph
    print "\t".join([send, "s", recv, doc_id])
    # emit co-occurring terms, with pairs in canonical order
    # (lower triangle of the cross-product)
    for i in range(0, len(term_list)):
        term = term_list[i]
        if not term in stopwords:
            print "\t".join([term, "f", "%.5f" % term_freq[term], doc_id])

            for j in range(0, len(term_list)):
                if i != j:
                    co_term = term_list[j]
                    if not co_term in stopwords:
                        print "\t".join([term, "c", co_term, doc_id])


def main(stopword_src):
    stopwords = getStopWords(stopword_src)
    # data_dir = "data/result1.txt"
    # file = open(data_dir, 'rb')
    # for line in file:
    for line in sys.stdin:
        parts = line.split("\t")
        fileName, message_id, date, send, recv = parts[0], parts[1], parts[2], parts[3], parts[4]
        doc_id = getUUID(fileName)
        term_count, word_bag = parseMsg(parts[5])
        term_list = getTermList(word_bag)
        term_freq = getTermFreq(term_count, term_list)
        emit(fileName, doc_id, date, send, recv, term_list, term_freq, stopwords)


if __name__ == "__main__":
    stopword_src = sys.argv[1] # "data/stopwords.txt"
    main(stopword_src)
