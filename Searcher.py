from PagerankFinal import *
from Trie import *
import pickle

normMatrix, nodeMap = pickle.load(open("./pagerankVals",'rb'))
globTrie, validDocs = pickle.load(open("./tfidfVals",'rb'))

def TFIDFPageRank(count, globcount, tfDict):
    try:
        idf = np.log(globcount/count)
        a = {}
        for i in tfDict:
            if normMatrix[i] == 0:
                a[i] = 0
                continue

            a[i] = (0.8*tfDict[i]*idf) + (0.2*normMatrix[i])
        return a
    except:
        return 0