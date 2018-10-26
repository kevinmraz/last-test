# -*- coding: utf-8 -*-
"""
Created on Wed May 16 14:44:21 2018

@author: kevinmraz
"""
#change1~
#change2~!!
import copy
import itertools
def f_1(T):
    return list(set(T))
def apriori(D,min_sup):
    C1={}
    for T in D:
        T_filter=f_1(T)
        for i in T_filter:
            if i in C1:
                C1[i]+=1
            else:
                C1[i]=1                
    keys=C1.keys()
    L1=[];
    for i in range (len(keys)):
        if float(C1[keys[i]])/len(D) >= min_sup:
            L1.append([keys[i]])
    allkey=[]
    for i in range(len(L1)):
        allkey.append(L1[i])
    key=L1
    while len(key)!=0:#key是频繁项集，C是候选项集，apriori_gen是由频繁项集产生候选项集，再通过扫描D，来由C产生新的key。
        C=apriori_gen(key)#C=[[a,c],[a,b]]/C=[[a,b,c],[a,b,d]]    
        array=[]
        for i in range(len(C)):
            count=0
            set1=set(C[i])#利用set集合判断一个列表的内容是否是另一个列表的子集
            for j in range(len(D)):
                set2=set(D[j])
                if set1.issubset(set2):
                    count+=1
                   
            if count*1.0/len(D)<min_sup:
                array.append(C[i])
        for l in range(len(array)):
            C.remove(array[l])       
        for x in range(len(C)):
            if C[x] not in allkey:
                allkey.append((C[x]))               
        key=C
    return allkey
        
def apriori_gen(key):#传来长度为len(key)的频繁k项集，需要将有k-1项相同的项两两组合形成新的k+1项集，并判断k+1项集的任意k项是频繁的。
    C=[]
    key1=copy.deepcopy(key)
    for a in key1:
        for b in key1:
            if a!=b:
                c=[]
                a.sort()
                b.sort()
                for k1 in a:
                    if k1 not in c:
                        c.append(k1)
                for k2 in b:
                    if k2 not in c:
                        c.append(k2)             
                if has_infrequent_subset(c,key)==False:
                    c.sort()
                    if c not in C:
                        C.append(c)
    return C               
                    
def has_infrequent_subset(c,key):
    flag=0
    store=copy.deepcopy(c)
    for i in range(len(c)):
        c=store[:]
        del c[i]
        set1=set(c)
        for j in range(len(key)):#只要有一个是子集，就验证下一个
            set2=set(key[j])
            if set1.issubset(set2):
                flag=0
                break
            else:
                flag=1
        if flag==1:
            return True
    return False

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
#dict1={'a':'健康麦香包','b':'皮蛋瘦肉粥','c':'养颜红枣糕','d':'八宝粥','e':'香煎葱油饼'}
#D = [['a','b','c'],['e','b','d'],['a','e','b','d'],['e','d']]
#D=[['m','o','n','k','e','y'],['d','o','n','k','e','y'],['m','a','k','e'],['m','u','c','k','y'],['c','o','o','k','i','e']]
#D=[['a','b','e'],['b','d'],['b','c'],['a','b','d'],['a','c'],['b','c'],['a','c'],['a','b','c','e'],['a','b','c']]
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
F = apriori(D, 0.3)
#print F
#for i in range(len(F)):
#    print '[',
#    for j in range(len(F[i])):
#        print dict1[F[i][j]],
#    print ']'
table=relation(F,0.8)
#for i in table:
#    print i