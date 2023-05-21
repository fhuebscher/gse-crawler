from Pagerank import *
from Trie import *
import pickle


def TFIDFPageRank(count, globcount, tfDict):
    try:
        idf = np.log(globcount/count)
        a = {}
        #top 10 tf values
        cutoff = sorted(tfDict, key=lambda x: tfDict[x], reverse=True)[:10]
        for i in tfDict:
            #Make all pages not in top 10 tf insignificant
            if i not in cutoff:
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
        trieNode.pageCount[i] = trieNode.pageCount[i] + (0.5*a[i])

    return trieNode.pageCount


normMatrix, nodeMap = pickle.load(open("data_store/pagerankVals",'rb'))
globTrie, validDocs = pickle.load(open("data_store/tfidfVals",'rb'))

#Parent nodes inherit a portion of child node values, basically math is gets a tf value if maths has a tf value on the page
TFInheritance(globTrie.root)
