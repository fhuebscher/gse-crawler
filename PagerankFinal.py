import numpy as np
from collections import defaultdict
import pickle

normMatrix, nodeMap= pickle.load(open("data_store/pagerankVals",'rb'))

if __name__ == "__main__":        
    #Setup
    path = "datasets/CaliforniaGraph/CaliforniaGraph"

    #Mapping from node to page
    nodeMap = {}
    #A storage space for edges, key is the pointer and in the list are the nodes being pointed at
    edgeMap = defaultdict(list)

    #Amount of nodes
    N = 9664

    #Each list in the list shows what index node transitions to it.
    #Each column must add up to 1, each column is the out going transitions of that columns node
    with open(path,'r') as f:
        for l in f.readlines():
            if l:
                a = l[:-1].split(" ")

                if a[0] == 'n':
                    nodeMap[int(a[1])] = a[2]
                else:
                    edgeMap[int(a[1])].append(int(a[2]))


    tMatrix = np.zeros((N,N))

    for i in edgeMap:
        if len(edgeMap[i]) > 0:
            val = 1/len(edgeMap[i])
            for l in edgeMap[i]:
                tMatrix[l][i] = val


    #An initial pagerank value matrix for the nodes
    nMatrix = np.array([1/N for i in range(N)]).T

    #A matrix multiplication to see what each column adds up to, and then inverting it. This is basically to see what columns add up to 0. Basically dangling nodes.
    #We then make those dangling node columns equal the value of 1/N and all others 0. This is so we can add it to the transition matrix to make the system closed.
    sumCol = (np.ones((N,1)) - np.dot(tMatrix.T,np.ones((N,1))))/N
    sumCol = np.repeat(sumCol, N, axis=1).T

    #We force the transition matrix to be a closed system, by making any dead end pages split up their rank across every page on the internet. Thus preventing a leak.
    #Basically the web server reaches the end of their journey and starts a new one from a random point
    tMatrixClosed = tMatrix + sumCol



    #Now we create a matrix out of the tMatrix that has a dampening factor
    d = 0.85
    #We also add a base probability of just switching page (atleast when looking at page rank as a web surfer)
    #This gives each node a base minimum unchanging value
    mMatrix = d*tMatrixClosed + (1-d)*np.full((N,N),1/N)

    for i in range(55):
        nMatrix = np.dot(mMatrix,nMatrix)

    #Normalize the matrix between 0 and 1
    mi = np.min(nMatrix)
    ma = np.max(nMatrix)

    normMatrix = (nMatrix - mi)/(ma - mi)

    pickle.dump([normMatrix,nodeMap], open('data_store/pagerankVals','wb'))

    a = sorted(enumerate(normMatrix),key=lambda x:x[1],reverse=True)
    for i in range(50):
        print(nodeMap[a[i][0]], a[i][1])
    

