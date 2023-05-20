from PagerankFinal import *
from Trie import *
from web_scraper import *
import pickle
import threading
# import multiprocessing

globTrie = Trie()
validDocs = 0

def insertPage(i):
    d = {}
    wordC = 0

    try:
        info = Get_info(nodeMap[i])
    except:
        return

    if len(info['text']) == 0 and len(info['titles']) == 1:
        return

    global validDocs
    global globTrie
    validDocs += 1

    for line in info['text']:
        lsplit = line.split(" ")

        for word in lsplit:
            word = word.lower()
            try:
                d[word].addCount(i, 1)
            except:
                #The insert adds to the Trie document counter for the word
                d[word] = globTrie.insert(word)
                d[word].addCount(i, 1)

            wordC +=1


    for line in info['section_titles']:
        lsplit = line.split(" ")

        for word in lsplit:
            word = word.lower()
            try:
                d[word].addCount(i, 2)
            except:
                #The insert adds to the Trie document counter for the word
                d[word] = globTrie.insert(word)
                d[word].addCount(i, 2)

            wordC +=2


    for line in info['subtitles']:
        lsplit = line.split(" ")

        for word in lsplit:
            word = word.lower()
            try:
                d[word].addCount(i, 3)
            except:
                #The insert adds to the Trie document counter for the word
                d[word] = globTrie.insert(word)
                d[word].addCount(i, 3)

            wordC +=1

    
    for line in info['titles']:
        lsplit = line.split(" ")

        for word in lsplit:
            word = word.lower()
            try:
                d[word].addCount(i, 4)
            except:
                #The insert adds to the Trie document counter for the word
                d[word] = globTrie.insert(word)
                d[word].addCount(i, 4)

            wordC +=4

    
    for words in d:
        #Calculates tf for the word in the page
        d[words].pageCount[i] = d[words].pageCount[i]/wordC


if __name__ == '__main__':
    #multiprocessing.set_start_method("fork")

    # pool = multiprocessing.Pool(processes=50)
    # pool.map(insertPage, [n for n in range(0,200)])

    atOnce = 500

    for i in range(0,9664,atOnce):
        tList = []
        for a in range(atOnce):
            x = threading.Thread(target=insertPage,args=(i+a,))
            tList.append(x)
            x.start()
        
        lC = i
        for thread in tList:
            print(lC)
            thread.join()
            lC += 1

    import sys

    max_rec = 0x100000

    sys.setrecursionlimit(max_rec)

    pickle.dump([globTrie, validDocs], open("tfidfVals",'wb'))