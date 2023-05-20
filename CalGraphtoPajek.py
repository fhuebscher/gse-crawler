with open("datasets/CaliforniaGraph/CaliforniaGraph",'r') as f:
    with open("datasets/CaliforniaGraph/CaliforniaGraph.net",'w') as w:
        nodeMode = True
        w.write("*Vertices 9664\n")
        for i in f.readlines():
            a = i[:-1].split(' ')
            if nodeMode and a[0] != 'n':
                nodeMode = False
                w.write("*Edges\n")
                continue

            if nodeMode:
                w.write(str(int(a[1]) + 1) + f' "{a[2]}"\n')
            else:
                w.write(str(int(a[1]) + 1) + f' {int(a[2]) + 1}\n')
