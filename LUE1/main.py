from __future__ import division
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import pickle
import preprocessor as pp

def getUnigramModel(data):
    model = {}
    for w in data:
        model[w] = model.get(w,0) + 1
    return model

def getNoiseFree(model, th):
    for k,v in model.items():
        if v < th:
            del model[k]
    return model

def getNoisyWords(model, th):
    for k,v in model.items():
        if v >= th:
            del model[k]
    return model.keys()

def printNoiseFreeModel(nfm):
    snfm = sorted(nfm.items(), key=lambda x:x[1],reverse=True)
    f = open('./data/snfm.txt','w+')
    for word, count in snfm:
        f.write(word+","+str(count)+"\n")

def extractTripletCount(cdata):
    tcount = {} #triplet and counts
    for tweet in cdata.split('\n'):
        if len(tweet) == 0: continue

        sentences = sent_tokenize(tweet)
        for sentence in sentences:
            words = word_tokenize(sentence)
            if len(words) >= 3:
                for i in range(len(words)-2):
                    triplet = (words[i], words[i+1], words[i+2])
                    tcount[triplet] = tcount.get(triplet, 0) + 1
    return tcount

def findScore(cpairs, tcount):
    scores = {}
    for pa, pb in cpairs:
        pa_list = []
        pb_list = []
        for t in tcount:
            if t[1] == pa:
                pa_list.append((t[0],t[2]))
            if t[1] == pb:
                pb_list.append((t[0],t[2]))
        ilist = set(pa_list).intersection(set(pb_list))
        print pa, pb
        print pa_list
        print pb_list
        print ilist
        print '-------------------------'

        if len(ilist) == 0:
            scores[pa+','+pb]=1; continue
        ca = 0
        cb = 0
        Z = 0
        D = 0
        for t in ilist:
            ca += tcount[(t[0], pa, t[1])]
            cb += tcount[(t[0], pb, t[1])]
            Z += ca + cb
            D += abs(ca-cb)
        scores[pa+','+pb]=(1-D/Z)
    return scores

def pickleTCount():
    f = open('./data/clean-tweets.txt')

    wordnet_lemmatizer = WordNetLemmatizer()

    # ToDo remove lower
    cdata = f.read().lower()

    lwords = word_tokenize(cdata)
    lemzlwords = []
    for word in lwords:
        lemzlwords.append(wordnet_lemmatizer.lemmatize(word))
    umodel = getUnigramModel(lemzlwords)

    # noisefree_umodel = getNoiseFree(umodel, THRESHOLD_COUNT)
    # printNoiseFreeModel(noisefree_umodel)

    THRESHOLD_COUNT = 5
    noisy_words = getNoisyWords(umodel, THRESHOLD_COUNT)
    for nw in noisy_words:
        cdata = cdata.replace(" " + nw + " ", ' SPL ')

    f = open('./data/lmz-clean-tweets.txt','w+')
    f.write(cdata)

    #tcount = extractTripletCount(cdata)
    #filehandler = open(b"./data/tcount.pkl", "wb")
    #pickle.dump(tcount, filehandler)

def loadTCount():
    file = open("./data/tcount.pkl", 'r')
    return pickle.load(file)

if __name__ == '__main__':
    # pickleTCount()
    # tcount = loadTCount()
    # f = open('./output/triplet-count.csv','w+')
    # for i,j in tcount.items():
    #     f.write("("+",".join(i)+")"+","+str(j))
    # chosen_pairs = [('narendra','bjp'),
    #                 ('modi','bjp'),
    #                 ('namo','narendra'),
    #                 ('raga','rahul'),
    #                 ('modi', 'dubai'),
    #                 ('rahul', 'congress'),
    #                 ('modi', 'bjp'),
    #                 ('bjp', 'rss'),
    #                 ('lion', 'roar'),
    #                 ('gujarat', 'muslim'),
    #                 ('dubai', 'crowd')]
    #
    # scores = findScore(chosen_pairs, tcount)
    # for i,j in scores.items():
    #     print i+':'+str(j)
    pp.