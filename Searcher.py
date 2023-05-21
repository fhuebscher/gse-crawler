from Pagerank import *
from Trie import *
import pickle

normMatrix, nodeMap = pickle.load(open("data_store/pagerankVals",'rb'))
globTrie, validDocs = pickle.load(open("data_store/tfidfVals",'rb'))

def TFIDFPageRank(count, globcount, tfDict):
    try:
        idf = np.log(globcount/count)
        a = {}
        for i in tfDict:
            if normMatrix[i] == 0 or tfDict[i] == 0:
                a[i] = 0
                continue

            a[i] = (0.9*tfDict[i]*idf) + (0.1*normMatrix[i])
        return a
    except:
        return 0
    

def TFInheritance(trieNode):
    if len(trieNode.children) < 1:
        return trieNode.pageCount

    if trieNode.is_end:
        divisor = 1/len(trieNode.children)
    else:
        divisor = 1

    a = defaultdict(float)
    for i in trieNode.children:
        d = TFInheritance(trieNode.children[i])
        for x in d:
            a[x] += divisor*d[x]

    if not trieNode.is_end:
        return a

    for i in a:
        trieNode.pageCount[i] = trieNode.pageCount[i] + (0.3*a[i])

    return trieNode.pageCount
