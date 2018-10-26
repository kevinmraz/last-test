# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:09:01 2018
change！！~

@author: kevinmraz
"""
import itertools
class treenode:
    def __init__(self,namevalue,numoccur,parentnode):
        self.name=namevalue
        self.count=numoccur
        self.nodelink=None
        self.parent=parentnode
        self.children={}
     
    def inc(self,numoccur):
        self.count+=numoccur

    def disp(self,ind = 1):
        print ' '*ind,self.name,' ',self.count
        for child in self.children.values():
            child.disp(ind+1)

def create_chart1(D,min_sup):
    C={}
    D_1={}
    for trans in D:
        s=frozenset(trans)#!!dict的key是集合必须frozenset
        if s not in D_1.keys():
            D_1[s]=0
        D_1[s]+=1
        for item in trans:
            if item in C:
                C[item]+=1
            else:
                C[item]=1    
    chart1={}
#    print D_1
    while(True):
        if len(C)==0:
            break
        t=max(C.items(),key=lambda x:x[1])
        if t[1]*1.0/len(D)>=min_sup:
            chart1[t[0]]=t[1]
            del C[t[0]]
        else:
            break
    for i in chart1:
        chart1[i]=[chart1[i],None]#!!!
    return chart1,D_1

def createtree(D_1,chart1):
   
    key_in_order=sorted(chart1.iteritems(),key=lambda d:d[1][0],reverse=True)
    for k in range(len(key_in_order)):
        key_in_order[k]=key_in_order[k][0]
    all_items_set=set(key_in_order)    
    root=treenode('null',1,None)
    for need_sort_trans in D_1:
        temp1=need_sort_trans & all_items_set
        temp=list(temp1)        
        sorted_trans=[item for item in key_in_order if item in temp]
        if(len(sorted_trans)!=0):        
            updatetree(sorted_trans,root,chart1,D_1[need_sort_trans])
    return root,key_in_order
def updatetree(items,root,chart1,count) :
    if items[0] in root.children:#????
        root.children[items[0]].inc(count)
    else:
        root.children[items[0]] = treenode(items[0], count, root)
        if chart1[items[0]][1] is None:
            chart1[items[0]][1] = root.children[items[0]]
        else:
            updateHeader(chart1[items[0]][1], root.children[items[0]])
    if len(items) > 1:
        updatetree(items[1:], root.children[items[0]], chart1, count)
    
            
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodelink is not None):
        nodeToTest = nodeToTest.nodelink
    nodeToTest.nodelink = targetNode

def ascendTree(leafNode, prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    # 对 treeNode的link进行循环
    while treeNode is not None:
        prefixPath = []
        # 寻找改节点的父节点，相当于找到了该节点的频繁项集
        ascendTree(treeNode, prefixPath)
        # 避免 单独`Z`一个元素，添加了空节点
        if len(prefixPath) > 1:
            # 对非basePat的倒叙值作为key,赋值为count数
            # prefixPath[1:] 变frozenset后，字母就变无序了
            # condPats[frozenset(prefixPath)] = treeNode.count
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        # 递归，寻找改节点的下一个 相同值的链接节点
        treeNode = treeNode.nodelink
        # print treeNode
    return condPats
def createfpree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k] < minSup*len(D):
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    retTree = treenode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:            
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updatetree(orderedItems, retTree, headerTable, count)

    return retTree, headerTable
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]

    for basePat in bigL:

        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createfpree(condPattBases, minSup)
        if myHead is not None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def relation(F,con_min):
    table=[]
    for f in F:
        if len(f)>=2:
            l=[]
            for i in range(len(f)-1):
                l.append(list(itertools.combinations(f,i+1)))
            for a in l:
                for i in range(len(a)):
                    s=set(f)
                    now=set(a[i])
                    left=s.difference(now)
                    count1=0
                    count2=0
                    for d in D:
                        s2=set(d)
                        if now.issubset(s2):
                            count1+=1
                        if  s.issubset(s2):
                            count2+=1
                    if count1==0:
                        print "wrong:",now,left
                    result=count2*1.0/count1
                    if result>=con_min:
                        str_=str(now)+"->"+str(left)+"  confidence:"+str(result)
                        table.append(str_)
    return table
D=[]
with open('C://Users//1-c//Desktop//supermarket.csv','r') as f1:
    items=f1.readline()
    items_list=items.split(',')
    items_list.pop()
    list1=f1.readlines()
    for l in list1:
        index=[]
        current_trans=[]
        l=l.rstrip('\n')
        l2=l.split(',')
        for i in range(len(l2)):
            if l2[i] == 't':
                index.append(i)
        for temp in index:
            current_trans.append(items_list[temp])
        D.append(current_trans)
f1.close()   
min_sup=0.3
min_conf=0.7
D_len=len(D)
chart1,D_1=create_chart1(D,min_sup)#建立表
tree,key_in_order=createtree(D_1,chart1)
freqItemList = []
mineTree(tree, chart1, min_sup, set([]), freqItemList)
for i in range(len(freqItemList)):
    freqItemList[i]=list(freqItemList[i])
table=relation(freqItemList,min_conf)    
for t in table:
    print t
