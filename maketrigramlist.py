#!usr/bin/env python3

import os
import sys
import collections
import argparse

#---------------------------------------------------------------------------------------#
#                                                    #
#    This program creates a trigram file, bigram file, and a word list        #    
#    that is used by FindManifold.py                                        #
#
#    Input is a corpus text with the filename <languagename>-<corpusname>.txt
#    (note the hyphen in the filename)
#
#    Begun by John Goldsmith and Wang Xiuli 2012.                           #
#    Jackson Lee 2015
#                                                    #
#---------------------------------------------------------------------------------------#

def makeArgParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--lang", help="Language name", type=str, default="english")
    parser.add_argument("--corpus", help="Corpus name (e.g. 'brown', 'google', 'encarta')", type=str, default="brown")
    parser.add_argument("--datapath", help="Data folder", type=str,
            default="../../data/")
    return parser

def main(argv):

    args = makeArgParser().parse_args()

    #---------------------------------------------------------------------------#
    #    Variables to be changed by user
    #---------------------------------------------------------------------------#

    language = args.lang
    corpus = args.corpus
    datafolder = args.datapath

    print('Language:', language)
    print('Corpus:', corpus)
    print('datafolder', datafolder)

    #---------------------------------------------------------------------------#
    #    File names
    #---------------------------------------------------------------------------#

    infolder = datafolder + language + '/'
    infilename         = infolder + language + '-' + corpus +  ".txt"
    outfolder        = infolder + 'ngrams/'

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    outfilenamePrefix = outfolder + language + '-' + corpus

    outfilename1     = outfilenamePrefix +  "_trigrams.txt"
#    outfilename2     = outfilenamePrefix +  "_alphabetized.trigrams.txt"
    outfilename3     = outfilenamePrefix +  "_words.txt"
    outfilename4     = outfilenamePrefix +  "_bigrams.txt" 
#    outfilename5     = outfilenamePrefix +  "_alphabetized.bigrams.txt"

    outfilebigrams1  = open(outfilename4, "w")
#    outfilebigrams2  = open(outfilename5, "w")
    outfiletrigrams1 = open(outfilename1, "w")
#    outfiletrigrams2 = open(outfilename2, "w")
    outfilewords      = open(outfilename3, "w")

    file1 = open(infilename)

    #---------------------------------------------------------------------------#
    #    Read file
    #---------------------------------------------------------------------------#

    wordDict            = collections.Counter()
    trigramDict         = collections.Counter()
    bigramDict            = collections.Counter()
    sep = "\t"

    print('Reading the corpus file now...')

    corpusSize = 0

    for line in file1:
        if not line:
            continue

        line = line.lower().replace('\n', '').replace('\r', '')

        line = line.replace(".", " .")
        line = line.replace(",", " ,")
        line = line.replace(";", " ;")
        line = line.replace("!", " !")
        line = line.replace("?", " ?")
        line = line.replace(":", " :")
        line = line.replace(")", " )")
        line = line.replace("(", "( ")

        words = line.split()

        corpusSize += len(words)

        for i in range(len(words)-2):

            word1 = words[i]
            word2 = words[i+1]
            word3 = words[i+2]

            wordDict[word1] += 1
            wordDict[word2] += 1
            wordDict[word3] += 1

            if i == 0:
                bigram = word1 + sep + word2
                bigramDict[bigram] += 1

            bigram = word2 + sep + word3
            trigram = word1 + sep + word2 + sep + word3

            trigramDict[trigram] += 1
            bigramDict[bigram] += 1        

            #--------------------------------------------------------------------


    print("\nCompleted counting words, bigrams, and trigrams.")
    file1.close()

    #---------------------------------------------------------------------------#
    #    Print output
    #---------------------------------------------------------------------------#
    intro_string = "# data source: " + infilename + "\n"

    print(intro_string, file=outfilewords)
    print(intro_string, file=outfiletrigrams1)
#    print(intro_string, file=outfiletrigrams2)
    print(intro_string, file=outfilebigrams1)
#    print(intro_string, file=outfilebigrams2)
     
    #------------------------------------------#
    #    sort bigrams, trigrams by frequency
    #------------------------------------------#

    topbigrams = [x for x in bigramDict.items()]
    topbigrams.sort(key=lambda x:x[1], reverse=True)

    toptrigrams = [x for x in trigramDict.items()]
    toptrigrams.sort(key=lambda x:x[1], reverse=True)

    for (bigram, freq) in topbigrams:
        print(bigram + "\t" +  str(freq), file=outfilebigrams1)

    for (trigram, freq) in toptrigrams:     
        print(trigram + "\t" + str(freq), file=outfiletrigrams1)

    print('bigram and trigram files (sorted by freq) ready')

    #------------------------------------------#
    #    alphabetize bigram, trigrams
    #------------------------------------------#

#    bigramlist = sorted(bigramDict.items())

#    for (bigram, freq) in bigramlist:
#        print(bigram + "\t" +  str(freq), file=outfilebigrams2)

#    trigramlist = sorted(trigramDict.items())

#    for (trigram, freq) in trigramlist:     
#        print(trigram + "\t" + str(freq), file=outfiletrigrams2)

#    print('bigram and trigram files (alphabetized) ready')

    #------------------------------------------#
    #    sort and print words
    #------------------------------------------#

    top_words = [x for x in wordDict.items()]
    top_words.sort(key=lambda x: x[1], reverse=True)

    for (word, freq) in top_words:
        print(word + " " + str(freq), file=outfilewords)

    print('wordlist file ready')

    #------------------------------------------#
    #    finish
    #------------------------------------------#

    print('\nCorpus word token size:', corpusSize)

    outfilewords.close()
    outfilebigrams1.close()
#    outfilebigrams2.close()
    outfiletrigrams1.close()
#    outfiletrigrams2.close()

if __name__ == "__main__":
    main(sys.argv)
