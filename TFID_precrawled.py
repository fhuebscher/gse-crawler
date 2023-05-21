from Pagerank import *
from Trie import *
from WebScraper import *
import pickle
import threading
import json
# import multiprocessing

globTrie = Trie()
crawler = WebScraper()
validDocs = 0

# precrawled data
input_file_path='datasets/CaliforniaGraph/CaliforniaGraph_crawling_processed.json'

with open(input_file_path) as file:
    json_data = json.load(file)

# add json.load_dump as optional parameter
def insertPage(i):
    d = {}
    wordC = 0

    # Scrape web pages
    try:
        info = json_data[str(i)]
        print(info)
        # get content from json dict which has been loaded previously
    except Exception as e:
        print(e)
        return

    if len(info)==0:
        return

    global validDocs
    global globTrie
    validDocs += 1

    if 'text' in info:
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

    if 'section_titles' in info:
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

    if 'subtitles' in info:
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

    if 'titles' in info:
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

    # check with saved json dump
    tfid_data_store_path = 'data_store/tfidfVals_precrawled'

    pickle.dump([globTrie, validDocs], open(tfid_data_store_path,'wb'))